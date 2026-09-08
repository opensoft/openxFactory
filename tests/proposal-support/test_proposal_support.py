"""Proposal supporting-document lifecycle tests."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "proposal-support.py"
PIN = REPO_ROOT / "contracts" / "openspec-cli-pin.yaml"
spec = importlib.util.spec_from_file_location("proposal_support", SCRIPT)
support = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = support
spec.loader.exec_module(support)

# The bytes a fictional registry serves in place of the published artifact. The
# pin the double writes records their REAL SHA-512 and SHA-1, so
# `verify_artifact` does real hashing over real bytes on every archive test
# below; only the registry is invented.
PINNED_CLI_PAYLOAD = b"a synthetic tarball standing in for @fission-ai/openspec"


def serve_a_fictional_registry(test: unittest.TestCase) -> list:
    """Give the archive wrapper a PINNED CLI without touching the network.

    WHY THE THREE ARCHIVE TESTS BELOW NEED THIS AT ALL. Since #691 the wrapper
    resolves its `openspec` THROUGH `contracts/openspec-cli-pin.yaml` — it
    fetches the published tarball, hashes it against the recorded content
    address and installs it — instead of running whatever the shell finds. That
    is the property those tests now depend on, and satisfying it literally would
    mean a registry round trip from a unit test, which this suite's hermeticity
    posture refuses (`tests/openspec_cli_pin/test_openspec_cli_pin.py` states
    the same rule and takes the same route).

    So the fiction is installed at the SUBPROCESS BOUNDARY of the verifier
    module `proposal-support.py` loads, exactly as the sibling suite does: the
    real `fetch_artifact` shells out, the real `verify_artifact` hashes real
    bytes against a pin that really records their address, the real
    `resolve_pinned` caches by that address, and the real
    `assert_reported_version` asks the resolved binary what it is. What the
    fictional `npm install` puts at the resolved path is a SHIM that forwards to
    the `openspec` on PATH — the binary these tests have always driven, and the
    reason for their `skipUnless` guard — so the archive they assert about is
    still performed by a real CLI, reached only through the pin's own resolver.

    Returns the recorded npm argv lists, so a caller may assert WHAT was run.
    """
    # ITS OWN directory, never the fixture root: the synthetic pin and the
    # install cache are the double's furniture, and a governance tool's
    # repository root is not the place to leave furniture.
    holder = TemporaryDirectory()
    test.addCleanup(holder.cleanup)
    workspace = Path(holder.name)

    verifier = support.pin_verifier()
    real_pin = verifier.read_pin(PIN)
    version = verifier.pinned_version(real_pin)
    binary = verifier.pinned_binary(real_pin)
    forwarded = shutil.which(binary)
    assert forwarded is not None, "guarded by skipUnless"

    digest = base64.b64encode(hashlib.sha512(PINNED_CLI_PAYLOAD).digest()).decode()
    # THE SYNTHETIC PIN NEEDS A SYNTHETIC LOCKFILE, since
    # `pin-openspec-cli-dependency-closure` (2026-09-08): the closure is
    # verified before anything is installed, and the lockfile's own entry for
    # the package must carry the pin's integrity. Written beside the pin,
    # because that is where `lockfile:` resolves.
    package = verifier.pinned_package(real_pin)
    lockfile_name = "synthetic.package-lock.json"
    lockfile_body = (json.dumps({
        "name": "openspec-cli-pin-closure", "version": "0.0.0",
        "lockfileVersion": 3, "requires": True,
        "packages": {
            "": {"name": "openspec-cli-pin-closure", "version": "0.0.0",
                 "dependencies": {package: version}},
            f"node_modules/{package}": {
                "version": version,
                "resolved": (f"https://registry.npmjs.org/{package}/-/"
                             f"openspec-{version}.tgz"),
                "integrity": f"sha512-{digest}",
                "bin": {binary: "bin/openspec.js"}},
        }}, indent=2) + "\n").encode("utf-8")
    (workspace / lockfile_name).write_bytes(lockfile_body)
    lockfile_digest = base64.b64encode(
        hashlib.sha512(lockfile_body).digest()).decode()
    pin_path = workspace / "pin.yaml"
    pin_path.write_text(
        "# a synthetic pin, in the real pin's own grammar\n"
        "schema_version: 1\n"
        "kind: pinned_contract_manifest\n"
        f"package: \"{verifier.pinned_package(real_pin)}\"\n"
        "source_repository: Fission-AI/OpenSpec\n"
        "registry: https://registry.npmjs.org\n"
        f"version: \"{version}\"\n"
        "revision_kind: package_integrity\n"
        "integrity_algorithm: sha512\n"
        f"integrity: \"sha512-{digest}\"\n"
        f"shasum: \"{hashlib.sha1(PINNED_CLI_PAYLOAD).hexdigest()}\"\n"
        f"binary: {binary}\n"
        f"lockfile: {lockfile_name}\n"
        f"lockfile_integrity: \"sha512-{lockfile_digest}\"\n"
        "lockfile_packages: \"1\"\n"
        "verify_pin: scripts/validate-openspec-cli-pin.py\n"
        "consumer_entrypoint: scripts/validate-openspec-cli-pin.py\n",
        encoding="utf-8")

    calls: list = []
    real_which = shutil.which
    # A real file under the double's own directory, never a hard-coded system
    # path: the constitution forbids a host-absolute path in a committed file
    # (§ IV), and `fetch_artifact` only asks whether npm is obtainable at all.
    fake_npm = workspace / "bin" / "npm"
    fake_npm.parent.mkdir(parents=True, exist_ok=True)
    fake_npm.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_npm.chmod(0o755)

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        calls.append(argv)
        if argv[1:2] == ["pack"]:
            destination = Path(argv[argv.index("--pack-destination") + 1])
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "openspec.tgz").write_bytes(PINNED_CLI_PAYLOAD)
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["ci"]:
            # `npm ci` installs a PROJECT in a working directory, so the double
            # reads `cwd` the way the real one does and the executable lands
            # where a project's does — `node_modules/.bin/<binary>`.
            prefix = Path(kwargs["cwd"])
            binaries = prefix / "node_modules" / ".bin"
            binaries.mkdir(parents=True, exist_ok=True)
            shim = binaries / binary
            shim.write_text(f'#!/bin/sh\nexec "{forwarded}" "$@"\n',
                            encoding="utf-8")
            shim.chmod(0o755)
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["--version"]:
            return subprocess.CompletedProcess(argv, 0, version + "\n", "")
        return subprocess.CompletedProcess(argv, 0, "", "")

    def restore(target, attribute, previous):
        setattr(target, attribute, previous)

    for target, attribute, value in (
            (verifier, "PIN_PATH", pin_path),
            (verifier, "_run", fake_run),
            (shutil, "which",
             lambda name, *a, **k: (str(fake_npm) if name == "npm"
                                    else real_which(name, *a, **k))),
    ):
        previous = getattr(target, attribute)
        test.addCleanup(restore, target, attribute, previous)
        setattr(target, attribute, value)

    previous_cache = os.environ.get("OPENSPEC_CLI_PIN_CACHE")

    def restore_cache():
        if previous_cache is None:
            os.environ.pop("OPENSPEC_CLI_PIN_CACHE", None)
        else:
            os.environ["OPENSPEC_CLI_PIN_CACHE"] = previous_cache

    test.addCleanup(restore_cache)
    # The install goes under the double's own directory, so a unit test never
    # writes into the developer's real pin cache.
    os.environ["OPENSPEC_CLI_PIN_CACHE"] = str(workspace / "cache")

    # The wrapper memoizes ONE resolution per process, keyed by the pin file;
    # cleared on both sides so neither a previous test's fiction nor this one's
    # can be answered from a cache built under different bytes.
    support._RESOLVED_OPENSPEC.clear()
    test.addCleanup(support._RESOLVED_OPENSPEC.clear)
    return calls


# --------------------------------------------------------------------------
# GIT FIXTURE HELPERS
#
# The archive gate's origin baseline is REAL GIT HISTORY — the declaration the
# packet's `.openspec.yaml` carried at the first commit whose `proposal.md`
# declares `Status: ratified` — so a fixture that exercises it has to be a
# repository with that history in it, not a directory of files. Shared by the
# retention tests below and by the three archive-wrapper tests above, which
# drive the same gate through the real `openspec` binary.
# --------------------------------------------------------------------------


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


def commit_all(root: Path, message: str) -> None:
    git(root, "add", "-A")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
        "commit", "-q", "-m", message)


def ratify(proposal: Path) -> None:
    """Flip the packet's own lifecycle header to `ratified`.

    The commit that carries this flip is the RATIFYING COMMIT the gate
    resolves, and the origin declaration standing in the tree at that moment
    is the baseline every later read is compared against.
    """
    text = proposal.read_text(encoding="utf-8")
    assert "Status: draft" in text
    proposal.write_text(text.replace("Status: draft", "Status: ratified", 1),
                        encoding="utf-8")


class ProposalSupportTests(unittest.TestCase):
    def fixture(self, root: Path) -> None:
        (root / "openspec/changes/change-a").mkdir(parents=True)
        topic = root / "ideation/staging/topic-a"
        topic.mkdir(parents=True)
        (root / "ideation/brainstorm").mkdir(parents=True)
        (root / "ideation/brainstorm/source.md").write_text(
            "# Source\n\nStatus: brainstorm\n"
        )
        (topic / "one.md").write_text(
            "# One\n\nStatus: staged\nKind: architecture\n\n"
            "[source](../../brainstorm/source.md)\n"
        )
        (topic / "two.md").write_text(
            "# Two\n\nStatus: record\nKind: report\n"
        )

    def test_dry_run_does_not_move(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, False,
            )
            self.assertEqual(len(manifest["files"]), 2)
            self.assertTrue((root / "ideation/staging/topic-a/one.md").exists())
            self.assertFalse((root / "openspec/changes/change-a/supporting-docs").exists())

    def test_complete_transition_updates_status_links_and_manifest(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], "nlm-1",
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            text = (destination / "one.md").read_text()
            self.assertIn("Status: draft", text)
            self.assertIn("Proposed by: change-a", text)
            self.assertIn("../../../ideation/brainstorm/source.md", text)
            self.assertIn("Status: record", (destination / "two.md").read_text())
            manifest = support.load_manifest(destination / "manifest.yaml")
            self.assertEqual(manifest["notebook_workspace"], "nlm-1")
            self.assertEqual(manifest["remaining_paths"], [])
            source = "# One\n\nStatus: staged\nKind: architecture\n\n" \
                "[source](../../brainstorm/source.md)\n"
            self.assertEqual(
                manifest["files"][0]["source_sha256"],
                hashlib.sha256(source.encode()).hexdigest(),
            )
            self.assertNotEqual(
                manifest["files"][0]["source_sha256"],
                manifest["files"][0]["sha256"],
            )
            snapshot = destination / manifest["files"][0]["source_snapshot_path"]
            self.assertEqual(snapshot.read_text(), source)
            self.assertFalse((root / "ideation/staging/topic-a").exists())
            self.assertEqual(support.verify_active_support(destination.parent), [])

    def test_the_recorded_origin_path_has_one_posix_spelling(self):
        """The origin path is a MACHINE-READABLE RECORD readers split on `/`:
        `generator._declared_origin_staging` resolves the demote's destination
        topic from it, and doc-health's `proposal-origin` family joins it to a
        repo root. `str(PurePath)` would spell it `ideation\\staging\\topic-a` on
        a Windows checkout, so the record would depend on the operating system of
        whoever ran the gate (Copilot, PR #221). Recorded twice in the manifest,
        so the two spellings are pinned EQUAL as well as POSIX — a manifest must
        not contradict itself about the path it came from."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
        self.assertEqual(manifest["origin"]["path"], "ideation/staging/topic-a")
        self.assertEqual(manifest["origin_path"], manifest["origin"]["path"])
        self.assertNotIn("\\", manifest["origin"]["path"])

        # STRUCTURAL, and deliberately so: on POSIX `str(PurePath)` and
        # `as_posix()` return the same string, so the assertions above cannot
        # tell the two apart and a regression to `str()` would pass them on
        # every Linux CI run — the defect only appears on the platform the suite
        # does not execute. So the SOURCE is pinned instead: the origin path is
        # derived once, via `as_posix()`, and the manifest's second copy reuses
        # that one value rather than re-deriving it.
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("origin_rel = source.relative_to(root).as_posix()", source)
        self.assertIn('"origin_path": origin_rel,', source)
        self.assertNotIn('"path": str(source.relative_to(root))', source)
        self.assertNotIn('"origin_path": str(source.relative_to(root))', source)

    def nested_fixture(self, root: Path) -> None:
        """A staging topic with a SUBFOLDER.

        The flat `fixture` above records `one.md` for `path` and
        `source-snapshots/one.md` for the snapshot — a file name with no
        separator has no spelling to get wrong, so it cannot show the defect.
        One level of nesting makes every recorded field carry a separator."""
        (root / "openspec/changes/change-a").mkdir(parents=True)
        notes = root / "ideation/staging/topic-a/notes"
        notes.mkdir(parents=True)
        (notes / "one.md").write_text(
            "# One\n\nStatus: staged\nKind: architecture\n"
        )
        (root / "ideation/staging/topic-a/two.md").write_text(
            "# Two\n\nStatus: record\nKind: report\n"
        )

    def commit_fixture(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c",
             "user.email=test@example.invalid", "commit", "-qm", "fixture"],
            cwd=root, check=True,
        )

    def test_every_recorded_manifest_path_has_one_posix_spelling(self):
        """The `files[]` and `remaining_paths` half of the same defect the
        origin path was fixed for (PR #221 named these fields as the next lap).

        Each is a machine-readable KEY beside a content hash: `path` and
        `source_snapshot_path` are joined to the support folder to find the
        file the sha256 describes, `source_path` becomes `<revision>:<path>`
        for `git show`, and `remaining_paths` names what stayed staged. Spelled
        by `str(PurePath)` on a Windows checkout they carry backslashes, so the
        keys — never the hashes — would depend on the writer's operating
        system, and a manifest verified anywhere else would report every entry
        missing."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.nested_fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", ["notes/one.md"],
                None, "2026-07-09", False, True,
            )
        entry = manifest["files"][0]
        self.assertEqual(entry["path"], "notes/one.md")
        self.assertEqual(entry["source_path"],
                         "ideation/staging/topic-a/notes/one.md")
        self.assertEqual(entry["source_snapshot_path"],
                         "source-snapshots/notes/one.md")
        self.assertEqual(manifest["remaining_paths"],
                         ["ideation/staging/topic-a/two.md"])
        for value in (*entry.values(), *manifest["remaining_paths"]):
            self.assertNotIn("\\", value)

        # STRUCTURAL, and the only assertions here that can fail on Linux: on
        # POSIX `str(PurePath)` and `as_posix()` return the SAME string, so
        # every value assertion above passes on a writer reverted to `str()`
        # and the defect appears only on the platform this suite never runs on
        # (the platform-inert mutation class PR #221 recorded). So the SOURCE is
        # pinned: each field is derived once, through `as_posix()`, and the
        # committed-blob check reads `entry["source_path"]` back rather than
        # deriving that path a second time — one derivation per path, so an
        # entry cannot contradict itself.
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn(
            '"path": mapping[path].relative_to(destination).as_posix(),',
            source)
        self.assertIn('"source_path": path.relative_to(root).as_posix(),',
                      source)
        self.assertIn(
            "snapshots[path].relative_to(destination).as_posix(),", source)
        self.assertIn('"remaining_paths": [path.relative_to(root).as_posix()',
                      source)
        self.assertIn('entry["source_path"])', source)
        self.assertNotIn("str(path.relative_to(root))", source)
        self.assertNotIn("str(mapping[path].relative_to(destination))", source)
        self.assertNotIn("str(snapshots[path].relative_to(destination))",
                         source)

    def test_verify_tolerates_backslash_spelled_manifest_paths(self):
        """Fixing the writer cannot reach a manifest already on disk, so the
        reader normalizes rather than assuming its own spelling — the same
        treatment `origin_errors` and `generator._declared_origin_staging`
        already give the origin path. Both fields are exercised because each is
        a separate lookup: one finds the transitioned file, the other the
        byte-exact snapshot the source hash is proved against."""
        for field in ("path", "source_snapshot_path"):
            with self.subTest(field=field), TemporaryDirectory() as td:
                root = Path(td)
                self.nested_fixture(root)
                support.transition(
                    root, "change-a", "ideation/staging/topic-a", [], None,
                    "2026-07-09", False, True,
                )
                directory = root / "openspec/changes/change-a"
                manifest_path = directory / "supporting-docs/manifest.yaml"
                manifest = support.load_manifest(manifest_path)
                entry = next(e for e in manifest["files"]
                             if "/" in e[field])
                entry[field] = entry[field].replace("/", "\\")
                manifest_path.write_text(support.manifest_text(manifest))
                self.assertEqual(
                    support.verify_active_support(directory), [])

    def test_git_blob_sha256_resolves_a_backslash_spelled_source_path(self):
        """The failure PR #221 named and deferred: a Windows-written manifest
        verified on Linux hands `git show` a `<revision>:a\\b\\c.md` that
        matches no tree entry, so the blob resolves to None and `verify`
        reports the source revision unavailable for a file that is right
        there."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.nested_fixture(root)
            self.commit_fixture(root)
            revision = support.repo_revision(root)
            rel = "ideation/staging/topic-a/notes/one.md"
            expected = support.sha256_file(root / rel)
            self.assertEqual(
                support.git_blob_sha256(root, revision, rel), expected)
            self.assertEqual(
                support.git_blob_sha256(root, revision, rel.replace("/", "\\")),
                expected)

    def test_verify_reconciles_a_backslash_source_path_against_the_revision(self):
        """End to end, with the snapshot deliberately out of the way: the
        committed blob is then the ONLY route to the recorded source hash, so
        this fails on an unnormalized `source_path` and cannot pass by
        accident through the snapshot check beside it."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.nested_fixture(root)
            self.commit_fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            directory = root / "openspec/changes/change-a"
            manifest_path = directory / "supporting-docs/manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            entry = next(e for e in manifest["files"]
                         if "/" in e["source_path"])
            entry["source_path"] = entry["source_path"].replace("/", "\\")
            del entry["source_snapshot_path"]
            manifest_path.write_text(support.manifest_text(manifest))
            self.assertEqual(support.verify_active_support(directory), [])

    def test_verify_archive_tolerates_backslash_spelled_manifest_paths(self):
        """The archived half of the round trip. Bundle member names are POSIX
        on every platform (`deterministic_bundle` writes `as_posix()`), so the
        manifest is the only side a Windows writer could spell otherwise — and
        an inventory comparison across two alphabets calls a sound bundle
        corrupt."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.nested_fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            support.package(root, "change-a", "2026-07-10", False, False, True)
            directory = root / "openspec/changes/change-a"
            manifest_path = directory / "supporting-docs.manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            self.assertEqual(support.verify_archive(directory), [])
            nested = [e for e in manifest["files"] if "/" in e["path"]]
            self.assertTrue(nested, "the fixture must record a nested path")
            for entry in nested:
                entry["path"] = entry["path"].replace("/", "\\")
            manifest_path.write_text(support.manifest_text(manifest))
            self.assertEqual(support.verify_archive(directory), [])

    def test_committed_source_checksum_is_verified(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm",
                 "fixture"], cwd=root, check=True,
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest_path = destination / "manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            manifest["files"][0]["source_sha256"] = "0" * 64
            manifest_path.write_text(support.manifest_text(manifest))
            errors = support.verify_active_support(destination.parent)
            self.assertTrue(any(
                "staging source checksum mismatch" in error
                for error in errors
            ))

    def test_source_snapshot_verifies_when_git_revision_is_unavailable(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm",
                 "fixture"], cwd=root, check=True,
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest_path = destination / "manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            manifest["source_revision"] = "f" * 40
            manifest_path.write_text(support.manifest_text(manifest))
            self.assertEqual(support.verify_active_support(destination.parent), [])

    def test_tampered_source_snapshot_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest = support.load_manifest(destination / "manifest.yaml")
            snapshot = destination / manifest["files"][0]["source_snapshot_path"]
            snapshot.write_text("tampered")
            errors = support.verify_active_support(destination.parent)
            self.assertTrue(any(
                "source snapshot checksum mismatch" in error for error in errors
            ))

    def test_partial_transition_leaves_remainder(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", ["one.md"],
                None, "2026-07-09", False, True,
            )
            self.assertTrue((root / "ideation/staging/topic-a/two.md").exists())
            self.assertEqual(
                manifest["remaining_paths"],
                ["ideation/staging/topic-a/two.md"],
            )

    def test_rejects_unsafe_and_broken_sources(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            with self.assertRaises(support.SupportError):
                support.transition(
                    root, "change-a", "ideation/staging/topic-a", ["../x"],
                    None, "2026-07-09", False, False,
                )
            (root / "ideation/staging/topic-a/one.md").write_text(
                "# One\n\nStatus: staged\n\n[missing](missing.md)\n"
            )
            with self.assertRaises(support.SupportError):
                support.transition(
                    root, "change-a", "ideation/staging/topic-a", ["one.md"],
                    None, "2026-07-09", False, False,
                )

    def test_archived_transition_preserves_superseded_status(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            archive = root / "openspec/changes/archive/2026-07-09-change-a"
            archive.mkdir(parents=True)
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "history.md").write_text(
                "# History\n\nStatus: superseded\nKind: reference\n"
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", True, True,
            )
            self.assertIn(
                "Status: superseded",
                (archive / "supporting-docs/history.md").read_text(),
            )

    def test_package_is_reproducible_and_verifiable(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            directory = root / "openspec/changes/change-a"
            first, _ = support.deterministic_bundle(directory / "supporting-docs")
            second, _ = support.deterministic_bundle(directory / "supporting-docs")
            self.assertEqual(first, second)
            support.package(
                root, "change-a", "2026-07-09", False, False, True
            )
            self.assertEqual(support.verify_archive(directory), [])
            bundle = directory / "supporting-docs.tar.gz"
            bundle.write_bytes(bundle.read_bytes() + b"corrupt")
            self.assertTrue(support.verify_archive(directory))

    @unittest.skipUnless(shutil.which("openspec"), "openspec CLI required")
    def test_archive_wrapper_preserves_bundle(self):
        npm = serve_a_fictional_registry(self)
        with TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(
                ["openspec", "init", str(root), "--tools", "none"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["openspec", "new", "change", "change-a"], cwd=root,
                check=True, capture_output=True, text=True,
            )
            change = root / "openspec/changes/change-a"
            (change / "proposal.md").write_text(
                "---\nStatus: draft\n---\n\n"
                "## Why\n\nTest archive support.\n\n"
                "## What Changes\n\n- Add test capability.\n\n"
                "## Capabilities\n\n### New Capabilities\n\n"
                "- `test-capability`: test\n\n"
                "### Modified Capabilities\n\n- None.\n\n"
                "## Impact\n\n- Tests only.\n"
            )
            (change / "design.md").write_text(
                "## Context\n\nTest.\n\n## Goals / Non-Goals\n\n"
                "**Goals:** archive.\n\n**Non-Goals:** none.\n\n"
                "## Decisions\n\nUse support bundle.\n\n"
                "## Risks / Trade-offs\n\nNone.\n"
            )
            spec_dir = change / "specs/test-capability"
            spec_dir.mkdir(parents=True)
            (spec_dir / "spec.md").write_text(
                "## ADDED Requirements\n\n"
                "### Requirement: Archive fixture\n"
                "The fixture SHALL archive.\n\n"
                "#### Scenario: Archive\n"
                "- **WHEN** the change archives\n"
                "- **THEN** the fixture MUST remain\n"
            )
            (change / "tasks.md").write_text(
                "## 1. Test\n\n- [x] 1.1 Complete fixture\n"
            )
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "source.md").write_text(
                "# Source\n\nStatus: staged\nKind: reference\n"
            )
            # A REPOSITORY, because the archive gate's origin baseline is
            # git history (`release-realization` § "Origin retention at
            # archive"): the declaration the packet carried at the commit that
            # ratified it. The commits below are the real sequence — the
            # packet and its staged topic land, the transition writes the
            # staged origin and moves the support, and the ratification lands
            # last, so the ratifying commit carries the origin the archive is
            # then checked against. `transition` also verifies its sources
            # against the committed blobs, which is why the topic is committed
            # before it runs rather than after.
            git(root, "init", "-q")
            commit_all(root, "create the packet and stage the topic")
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            commit_all(root, "move the support and declare the origin")
            ratify(change / "proposal.md")
            commit_all(root, "record the ratification")
            support.archive_change(
                root, "change-a", "2026-07-09", False, True
            )
            archived = list((root / "openspec/changes/archive").glob(
                "????-??-??-change-a"
            ))
            self.assertEqual(len(archived), 1)
            self.assertTrue((archived[0] / "supporting-docs.tar.gz").is_file())
            self.assertEqual(support.verify_archive(archived[0]), [])
            # …and it got there through the PIN: the artifact was fetched and
            # installed by the verifier's own resolver, which is a fact about
            # this run rather than an inference from its result.
            self.assertTrue(any(argv[1:2] == ["pack"] for argv in npm), npm)
            # `npm ci` and not `npm install`, since
            # `pin-openspec-cli-dependency-closure` (2026-09-08): the archive
            # act installs the PINNED DEPENDENCY CLOSURE through the committed
            # lockfile, and `npm install` would re-resolve the ranges the
            # lockfile exists to fix.
            self.assertTrue(any(argv[1:2] == ["ci"] for argv in npm), npm)

    @unittest.skipUnless(shutil.which("openspec"), "openspec CLI required")
    def test_archive_wrapper_archives_a_change_that_has_no_supporting_docs(self):
        """A staged-origin change that legitimately never took its topic with it
        MUST still archive through the sanctioned wrapper.

        The promoted rule scopes packaging to a change WITH supporting
        documents, and `verify` reads it that way on both sides — but this
        wrapper called `package()` unconditionally and died on
        "supporting-docs folder not found", which is the one thing that pushes
        an operator toward a bare `openspec archive` and around the gate.
        Fifteen archived staged-origin changes already have this shape."""
        serve_a_fictional_registry(self)
        with TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(
                ["openspec", "init", str(root), "--tools", "none"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["openspec", "new", "change", "change-b"], cwd=root,
                check=True, capture_output=True, text=True,
            )
            change = root / "openspec/changes/change-b"
            (change / "proposal.md").write_text(
                "---\nStatus: draft\n---\n\n"
                "## Why\n\nTest archive without support.\n\n"
                "## What Changes\n\n- Add test capability.\n\n"
                "## Capabilities\n\n### New Capabilities\n\n"
                "- `test-capability`: test\n\n"
                "### Modified Capabilities\n\n- None.\n\n"
                "## Impact\n\n- Tests only.\n"
            )
            spec_dir = change / "specs/test-capability"
            spec_dir.mkdir(parents=True)
            (spec_dir / "spec.md").write_text(
                "## ADDED Requirements\n\n"
                "### Requirement: Bundleless archive fixture\n"
                "The fixture SHALL archive without a bundle.\n\n"
                "#### Scenario: Archive\n"
                "- **WHEN** the change archives\n"
                "- **THEN** the fixture MUST remain\n"
            )
            (change / "tasks.md").write_text(
                "## 1. Test\n\n- [x] 1.1 Complete fixture\n"
            )
            # a STAGED origin, exactly as a topic-derived change carries — and
            # NO supporting-docs folder, exactly as one that left its topic
            # staged for a successor carries.
            (change / ".openspec.yaml").write_text(
                "schema: spec-driven\n"
                "created: 2026-07-09\n"
                "origin:\n"
                "  kind: staged\n"
                "  id: fixture:staging:topic-b\n"
                "  path: ideation/staging/topic-b\n"
                "  reason: the topic stays staged for a successor change\n"
                "  approved_by: fixture\n"
                "  approved_on: '2026-07-09'\n"
            )
            self.assertFalse((change / "supporting-docs").exists())
            # …and a real ratification in history, which the origin-retention
            # gate reads as the baseline for the declaration above.
            git(root, "init", "-q")
            commit_all(root, "create the packet")
            ratify(change / "proposal.md")
            commit_all(root, "record the ratification")

            support.archive_change(root, "change-b", "2026-07-09", False, True)

            archived = list((root / "openspec/changes/archive").glob(
                "????-??-??-change-b"
            ))
            self.assertEqual(len(archived), 1)
            # nothing was invented to satisfy the packager
            self.assertFalse((archived[0] / "supporting-docs.tar.gz").exists())
            self.assertFalse(
                (archived[0] / "supporting-docs.manifest.yaml").exists())
            # …and the origin still verifies on the archived side
            self.assertEqual(support.verify(root, "change-b"), [])

    @unittest.skipUnless(shutil.which("openspec"), "openspec CLI required")
    def test_final_import_complete_without_a_bundle_is_refused(self):
        """`--final-import-complete` records a NotebookLM import for a support
        bundle. With no bundle it records nothing, so it is refused rather than
        silently ignored."""
        serve_a_fictional_registry(self)
        with TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(
                ["openspec", "init", str(root), "--tools", "none"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["openspec", "new", "change", "change-c"], cwd=root,
                check=True, capture_output=True, text=True,
            )
            change = root / "openspec/changes/change-c"
            (change / "proposal.md").write_text(
                "---\nStatus: draft\n---\n\n"
                "## Why\n\nTest.\n\n## What Changes\n\n- Add.\n\n"
                "## Capabilities\n\n### New Capabilities\n\n"
                "- `test-capability`: test\n\n"
                "### Modified Capabilities\n\n- None.\n\n"
                "## Impact\n\n- Tests only.\n"
            )
            spec_dir = change / "specs/test-capability"
            spec_dir.mkdir(parents=True)
            (spec_dir / "spec.md").write_text(
                "## ADDED Requirements\n\n"
                "### Requirement: Fixture\n"
                "The fixture SHALL exist.\n\n"
                "#### Scenario: Archive\n"
                "- **WHEN** it archives\n"
                "- **THEN** it MUST remain\n"
            )
            (change / "tasks.md").write_text(
                "## 1. Test\n\n- [x] 1.1 Done\n"
            )
            (change / ".openspec.yaml").write_text(
                "schema: spec-driven\n"
                "created: 2026-07-09\n"
                "origin:\n"
                "  kind: ad_hoc\n"
                "  id: fixture:adhoc:2026-07-09-change-c\n"
                "  reason: fixture\n"
                "  approved_by: fixture\n"
                "  approved_on: '2026-07-09'\n"
            )
            git(root, "init", "-q")
            commit_all(root, "create the packet")
            ratify(change / "proposal.md")
            commit_all(root, "record the ratification")
            # assertRaisesRegex, NOT a bare assertRaises (F4): the PRE-fix
            # path also raised SupportError here — "supporting-docs folder not
            # found" — so a bare assertion passed against the very code this
            # test exists to pin, and proved nothing.
            with self.assertRaisesRegex(
                    support.SupportError, "final-import-complete"):
                support.archive_change(
                    root, "change-c", "2026-07-09", True, True)

    def test_a_status_line_inside_a_code_fence_is_an_example_not_the_status(self):
        """REGRESSION, 2026-08-15. The first fragment this mover ever moved
        carried a copy-pasteable template skeleton whose fenced example header
        read `Status: staged`. The verifier's multiline regex matched the
        EXAMPLE and failed a bundle whose real header the mover had already
        transitioned to `draft` — which would have blocked the archive gate on
        a bundle that was correct."""
        fenced = (
            "# Topic\n\nStatus: draft\nKind: reference\n\n"
            "Copy this skeleton:\n\n"
            "```markdown\n# Staged: <title>\n\nStatus: staged\nKind: reference\n```\n"
        )
        self.assertFalse(support._declares_staged_status(fenced))

        # ...and the real thing is still caught, outside any fence.
        real = "# Topic\n\nStatus: staged\nKind: reference\n"
        self.assertTrue(support._declares_staged_status(real))

        # An unclosed fence must not swallow a later real header.
        unclosed = "# Topic\n\n```\nexample\n```\n\nStatus: staged\n"
        self.assertTrue(support._declares_staged_status(unclosed))

    def test_a_moved_fragment_carrying_a_fenced_example_still_verifies(self):
        """The same defect end to end: transition a fragment whose body holds a
        fenced `Status: staged` example, then verify the bundle."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            topic = root / "ideation/staging/topic-a"
            (topic / "source.md").write_text(
                "# Source\n\nStatus: staged\nKind: reference\n\n"
                "```markdown\nStatus: staged\n```\n"
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-08-15", False, True,
            )
            moved = root / "openspec/changes/change-a/supporting-docs/source.md"
            self.assertIn("Status: draft", moved.read_text())
            self.assertEqual(
                support.verify_active_support(root / "openspec/changes/change-a"), [])


class AuthorshipRecordTests(unittest.TestCase):
    """`refine-demote-round-trip-mechanics` part 3: the proposal gate records its
    authorship ONCE PER DOCUMENT, not once per attempt.

    A document may legitimately reach proposal, be demoted, be worked, and reach
    proposal again — the round-trip guarantee exists precisely so that lap is
    normal. Appending a fresh `Proposed by:` line each time turns a normal lap
    into an ambiguous record: several lines each claiming to name the proposing
    change say nothing about which one is current.
    """

    def rendered(self, root: Path, text: str, change: str = "change-b") -> str:
        path = root / "doc.md"
        path.write_text(text, encoding="utf-8")
        return support.proposed_content(path, path, {}, root, change).decode("utf-8")

    def test_a_first_lap_adds_the_authorship_line(self):
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), "# One\n\nStatus: staged\nKind: reference\n")
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\nKind: reference\n")

    def test_a_second_lap_updates_the_line_rather_than_adding_another(self):
        """The shape a demoted document comes back in: the demote restores
        `Status: staged` and correctly leaves the authorship line alone, so the
        next transition sees both."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td),
                "# One\n\nStatus: staged\nProposed by: change-a\nKind: reference\n")
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\nKind: reference\n")
        self.assertEqual(out.count("Proposed by:"), 1)

    def test_a_third_lap_still_leaves_exactly_one_line(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            once = self.rendered(root, "# One\n\nStatus: staged\nKind: reference\n",
                                 "change-a")
            twice = self.rendered(root, once.replace("Status: draft", "Status: staged"),
                                  "change-b")
            thrice = self.rendered(root, twice.replace("Status: draft", "Status: staged"),
                                   "change-c")
        self.assertEqual(
            [line for line in thrice.splitlines() if line.startswith("Proposed by:")],
            ["Proposed by: change-c"])

    def test_the_update_preserves_a_crlf_documents_line_endings(self):
        """`.*$` and `\\s*$` both eat the `\\r` and leave the rewritten line LF in
        a CRLF file — the same corpus-integrity class the demote's move arm was
        fixed for. Rewriting a ROW in place keeps the ending it had, so BOTH lines
        this gate touches stay CRLF, not just the one the first fix covered."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td),
                "# One\r\n\r\nStatus: staged\r\nProposed by: change-a\r\n"
                "Kind: reference\r\n\r\nbody\r\n")
        self.assertEqual(
            out,
            "# One\r\n\r\nStatus: draft\r\nProposed by: change-b\r\n"
            "Kind: reference\r\n\r\nbody\r\n")
        # not one stray LF anywhere in a CRLF document
        self.assertNotIn("\n", out.replace("\r\n", ""))

    def test_a_crlf_document_gets_its_first_record_in_its_own_flavor(self):
        """The ADD arm through the same lens: the inserted line takes the status
        line's own ending, so a Windows-authored fragment does not come back with
        one LF in it."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td), "# One\r\n\r\nStatus: staged\r\nKind: reference\r\n")
        self.assertEqual(
            out,
            "# One\r\n\r\nStatus: draft\r\nProposed by: change-b\r\n"
            "Kind: reference\r\n")
        self.assertNotIn("\n", out.replace("\r\n", ""))

    def test_the_flip_does_not_eat_the_blank_line_below_the_header(self):
        """`^Status:\\s*staged\\s*$` consumes the newline after the header — `\\s*`
        is greedy and `$` is satisfied one line later — so a human's blank line
        between the header block and the body was DELETED on every lap. Pinned by
        line count as well as by text, because that is how it was noticed: seven
        lines in, six out."""
        source = "# One\n\nStatus: staged\n\nKind: reference\n\nbody\n"
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\n\n"
                 "Kind: reference\n\nbody\n")
        # the record is the ONLY line added: 7 in, 8 out, and no blank lost
        self.assertEqual(len(out.splitlines()), len(source.splitlines()) + 1)

    def test_the_update_arm_does_not_eat_the_blank_line_either(self):
        source = "# One\n\nStatus: staged\nProposed by: change-a\n\nbody\n"
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\n\nbody\n")
        self.assertEqual(len(out.splitlines()), len(source.splitlines()))

    # ---- fence-awareness and header anchoring (review C1) --------------------

    def test_a_fenced_example_record_is_not_the_documents_record(self):
        """A `Proposed by:` line inside a ``` block is an EXAMPLE — a skeleton
        somebody pasted in to show what a fragment looks like. Reading it as this
        document's record did two things at once: it SUPPRESSED adding the real
        record (against the ratified 'the record MUST be added'), and it silently
        rewrote somebody's example to name the current change."""
        source = ("# One\n\nStatus: staged\nKind: reference\n\n"
                  "Copy this skeleton:\n\n"
                  "```markdown\nStatus: staged\nProposed by: some-old-change\n```\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        # the real record was ADDED, in the header block
        self.assertEqual(
            [line for line in out.splitlines()
             if line.startswith("Proposed by:")][0], "Proposed by: change-b")
        # …and the fenced example is untouched, verbatim
        self.assertIn(
            "```markdown\nStatus: staged\nProposed by: some-old-change\n```\n", out)

    def test_a_fenced_status_example_is_not_the_documents_status(self):
        """The same blindness on the other header. A document whose FIRST
        `Status:` line is a fenced example must still be read by its own."""
        source = ("# One\n\n```markdown\nStatus: staged\n```\n\n"
                  "Status: staged\nKind: reference\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertIn("```markdown\nStatus: staged\n```\n", out)   # example intact
        self.assertIn("Status: draft\nProposed by: change-b\nKind: reference\n", out)

    def test_a_record_far_below_the_header_does_not_become_the_record(self):
        """Anchoring, not 'first match anywhere'. A `Proposed by:` line down in
        the prose is not this document's authorship record; rewriting it there
        left the header block with no record at all and quietly relocated a
        governance line into somebody's body text."""
        source = ("# One\n\nStatus: staged\nKind: reference\n\n"
                  "## History\n\nProposed by: change-a (a note about the past)\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        lines = [line for line in out.splitlines()
                 if line.startswith("Proposed by:")]
        self.assertEqual(lines, ["Proposed by: change-b"])
        # the record joined the HEADER BLOCK, under the status it belongs to
        self.assertIn("Status: draft\nProposed by: change-b\nKind: reference\n", out)

    # ---- duplicate collapse (review C3) -------------------------------------

    def test_pre_existing_duplicate_records_are_collapsed_to_one(self):
        """The ratified requirement is unconditional: 'the document MUST carry
        exactly one such record… naming the most recent attempt'. Refreshing one
        of three and leaving two stale satisfies the letter of an update and none
        of the point — several lines each claiming to name the proposing change
        say nothing about which one is current."""
        source = ("# One\n\nStatus: staged\nProposed by: change-a\n"
                  "Proposed by: change-x\nKind: reference\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\nKind: reference\n")

    def test_collapse_keeps_the_header_blocks_copy_and_drops_the_stray(self):
        source = ("# One\n\nStatus: staged\nProposed by: change-a\n"
                  "Kind: reference\n\n## History\n\nProposed by: change-x\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertEqual(
            [line for line in out.splitlines()
             if line.startswith("Proposed by:")], ["Proposed by: change-b"])
        self.assertIn("## History\n\n", out)

    def test_collapse_never_reaches_inside_a_fence(self):
        source = ("# One\n\nStatus: staged\nProposed by: change-a\n"
                  "Proposed by: change-x\nKind: reference\n\n"
                  "```\nProposed by: an-example\n```\n")
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), source)
        self.assertIn("```\nProposed by: an-example\n```\n", out)
        self.assertEqual(
            [line for line in out.splitlines()
             if line.startswith("Proposed by:")],
            ["Proposed by: change-b", "Proposed by: an-example"])

    def test_the_status_flip_still_happens_when_a_line_already_exists(self):
        """The status flip itself is unchanged by this part — the update arm must
        not become an arm that forgets to flip."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td), "# One\n\nStatus: staged\nProposed by: change-a\n")
        self.assertIn("Status: draft", out)
        self.assertNotIn("Status: staged", out)

    def test_a_non_staged_document_is_left_alone(self):
        """The gate only writes authorship on the staged->draft flip; a `record`
        document carrying its own historical line is not rewritten."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td), "# One\n\nStatus: record\nProposed by: change-a\n")
        self.assertIn("Proposed by: change-a", out)

    def test_the_end_to_end_round_trip_shape_carries_one_line(self):
        """Driven through `transition`, not just the renderer."""
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openspec/changes/change-b").mkdir(parents=True)
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "one.md").write_text(
                "# One\n\nStatus: staged\nProposed by: change-a\nKind: reference\n",
                encoding="utf-8")
            support.transition(root, "change-b", "ideation/staging/topic-a", [],
                               None, "2026-08-19", False, True)
            moved = (root / "openspec/changes/change-b/supporting-docs/one.md"
                     ).read_text(encoding="utf-8")
        self.assertEqual(
            [line for line in moved.splitlines() if line.startswith("Proposed by:")],
            ["Proposed by: change-b"])



class OriginRetentionAtArchiveTests(unittest.TestCase):
    """`release-realization` § "Origin retention at archive", issue #690.

    The requirement — "Mutation of an origin declaration after ratification
    SHALL be rejected at the archive gate" — had no running implementation
    until this gate: `origin_errors` reads presence and shape off the packet in
    front of it and cannot see what the change was ratified over, so PR #685
    edited the `approved_by` prose of an already-ratified packet and archived
    green.

    NONE of these tests needs the `openspec` binary, and that is the point of
    where the gate sits: it refuses BEFORE `openspec validate` and before any
    packaging, so a mutated origin never reaches the operation it would
    otherwise be archived by.
    """

    ORIGIN = (
        "origin:\n"
        "  kind: ad_hoc\n"
        "  id: fixture:adhoc:2026-09-05-change-r\n"
        "  reason: the fixture declares an ad-hoc origin\n"
        "  approved_by: >-\n"
        "    Fixture Authority, quoting the ratified prose\n"
        "  approved_on: '2026-09-05'\n"
    )
    STAGED_ORIGIN = (
        "origin:\n"
        "  kind: staged\n"
        "  id: fixture:staging:topic-r\n"
        "  path: ideation/staging/topic-r\n"
    )

    def packet(self, root: Path, *, change: str = "change-r",
               origin: str | None = ORIGIN, ratified: bool = True,
               manifest: dict | None = None,
               declare_origin_after_ratification: bool = False) -> Path:
        """A one-change repository whose ratifying commit is its second."""
        directory = root / "openspec" / "changes" / change
        directory.mkdir(parents=True)
        (directory / "proposal.md").write_text(
            "---\nStatus: draft\n---\n\n## Why\n\nFixture packet.\n",
            encoding="utf-8")
        (directory / "tasks.md").write_text(
            "## 1. Work\n\n- [x] 1.1 Done\n", encoding="utf-8")
        header = "schema: spec-driven\ncreated: 2026-09-05\n"
        if origin is not None and not declare_origin_after_ratification:
            (directory / ".openspec.yaml").write_text(header + origin,
                                                      encoding="utf-8")
        if manifest is not None:
            (directory / "supporting-docs").mkdir()
            (directory / "supporting-docs" / "manifest.yaml").write_text(
                support.manifest_text(manifest), encoding="utf-8")
        git(root, "init", "-q")
        commit_all(root, "create the packet")
        if ratified:
            ratify(directory / "proposal.md")
            commit_all(root, "record the ratification")
        if origin is not None and declare_origin_after_ratification:
            (directory / ".openspec.yaml").write_text(header + origin,
                                                      encoding="utf-8")
            commit_all(root, "backfill the origin declaration")
        return directory

    def mutate(self, directory: Path, old: str, new: str) -> None:
        packet = directory / ".openspec.yaml"
        text = packet.read_text(encoding="utf-8")
        self.assertIn(old, text)
        packet.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_an_unchanged_origin_passes_the_gate(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_the_resolved_ratifying_commit_is_the_one_that_flipped_the_header(self):
        """ANTI-VACUITY. A gate that resolved the wrong commit would compare
        the packet against itself and pass everything."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            self.assertEqual(
                support.ratifying_commit(root, "change-r"), head)

    def test_a_mutated_approval_prose_is_refused(self):
        """THE #685 SHAPE, reduced to a fixture: the approval provenance's
        prose is edited after ratification and the archive is attempted."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            errors = support.origin_retention_errors(root, directory)
            joined = "\n".join(errors)
            self.assertIn("changed keys: approved_by", joined)
            # the finding names the LINES, both halves
            self.assertIn("-    Fixture Authority, quoting the ratified prose",
                          joined)
            self.assertIn("+    Fixture Authority, quoting the corrected prose",
                          joined)
            self.assertIn(
                support.ratifying_commit(root, "change-r")[:12], joined)
            self.assertIn("contested-class act", joined)
            # …and the gate refuses the archive itself, not merely reports
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)

    def test_a_mutated_reason_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "the fixture declares an ad-hoc origin",
                        "a reason no authority ever approved")
            errors = support.origin_retention_errors(root, directory)
            joined = "\n".join(errors)
            self.assertIn("changed keys: reason", joined)
            self.assertIn("a reason no authority ever approved", joined)
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)

    def test_a_comment_added_after_ratification_is_a_changed_declaration(self):
        """The comparison is over the LINES, normalized for trailing
        whitespace and nothing else. A comment appended to the approval stamp
        leaves every scalar equal, so no key is named — and the block is still
        refused, on the diff, which is the honest answer rather than a
        silence."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "  approved_on: '2026-09-05'",
                        "  approved_on: '2026-09-05'   # stamped late")
            errors = support.origin_retention_errors(root, directory)
            self.assertTrue(errors)
            self.assertIn("stamped late", "\n".join(errors))

    def test_trailing_whitespace_alone_is_not_a_mutation(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "  approved_on: '2026-09-05'",
                        "  approved_on: '2026-09-05'   ")
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_a_never_ratified_change_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root, ratified=False)
            errors = support.origin_retention_errors(root, directory)
            self.assertIn("not ratified", "\n".join(errors))
            with self.assertRaisesRegex(support.OriginRetentionError,
                                        "not ratified"):
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)

    def test_a_fenced_status_example_does_not_ratify_a_packet(self):
        """A `Status: ratified` line inside a ``` block is an EXAMPLE. Reading
        one as the header would resolve a ratifying commit that ratified
        nothing, and the baseline the whole gate rests on would be a quotation
        — this corpus's proposals quote lifecycle headers constantly."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root, ratified=False)
            proposal = directory / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8")
                + "\n```\nStatus: ratified\n```\n", encoding="utf-8")
            commit_all(root, "quote a lifecycle header")
            self.assertIsNone(support.ratifying_commit(root, "change-r"))
            self.assertIn(
                "not ratified",
                "\n".join(support.origin_retention_errors(root, directory)))

    def test_a_staged_origin_id_moving_with_its_manifest_is_refused(self):
        """THE LOCKSTEP EDIT. `origin_errors` compares the packet against the
        support manifest, so moving BOTH copies leaves them agreeing with each
        other about the wrong thing and passes that check. The ratifying
        commit is the third copy neither edit can reach."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(
                root, origin=self.STAGED_ORIGIN,
                manifest={"format_version": 1, "files": [],
                          "origin": {"kind": "staged",
                                     "id": "fixture:staging:topic-r",
                                     "path": "ideation/staging/topic-r"}})
            self.mutate(directory, "fixture:staging:topic-r",
                        "fixture:staging:topic-s")
            manifest = directory / "supporting-docs" / "manifest.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "fixture:staging:topic-r", "fixture:staging:topic-s"),
                encoding="utf-8")
            # the shape gate is satisfied — the two copies agree
            self.assertEqual(
                support.origin_errors(
                    root, directory, strict=True,
                    manifest=support.load_manifest(manifest)),
                [])
            # …and the retention gate is not
            joined = "\n".join(
                support.origin_retention_errors(root, directory))
            self.assertIn("changed keys: id", joined)
            self.assertIn("support manifest origin `id`", joined)
            self.assertIn("fixture:staging:topic-r", joined)

    def test_a_packet_whose_ratifying_commit_declares_no_origin_is_not_refused(self):
        """NO BASELINE IS NOT A MUTATION. Four active changes on `main` carry an
        origin their ratifying commit does not — their lifecycle headers were
        written by one backfill and their origins by a later recorded sweep —
        and there is no original declaration for the current one to differ
        from. Presence and shape are still gated by `origin_errors`, and the
        nightly family still reports the missing-origin class."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(
                root, declare_origin_after_ratification=True)
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_an_origin_deleted_after_ratification_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            (directory / ".openspec.yaml").write_text(
                "schema: spec-driven\ncreated: 2026-09-05\n",
                encoding="utf-8")
            self.assertIn(
                "is GONE",
                "\n".join(support.origin_retention_errors(root, directory)))

    def test_an_unreadable_history_refuses_rather_than_skipping(self):
        """A check that cannot run MUST NOT pass. With no repository there is
        no ratifying commit to resolve, and answering "retained" would be an
        assertion nobody measured."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = root / "openspec" / "changes" / "change-r"
            directory.mkdir(parents=True)
            (directory / ".openspec.yaml").write_text(
                "schema: spec-driven\n" + self.ORIGIN, encoding="utf-8")
            # git DISCOVERS upwards, so "this directory is not a repository"
            # is only true until someone's TMPDIR sits inside a checkout. The
            # ceiling makes the fixture mean what it says on every machine.
            with mock.patch.dict(os.environ,
                                 {"GIT_CEILING_DIRECTORIES": str(root)}):
                errors = support.origin_retention_errors(root, directory)
            self.assertIn("history is unreadable", "\n".join(errors))

    def test_the_cli_refuses_with_exit_2_and_no_traceback(self):
        """The refusal is a STATUS a caller can branch on: 2 for a
        contested-class origin mutation, 1 for the shape errors an operator
        fixes and retries. And no traceback — a stack trace here would read as
        a crash in the gate rather than a finding from it."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "archive",
                 "change-r", "--yes"],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("origin retention", result.stderr)
            self.assertIn("no bypass flag", result.stderr)

    def test_every_arm_of_the_gate_exits_2_not_only_the_mutation(self):
        """THE EXIT STATUS IS THE GATE'S, NOT THE MUTATION'S. `not ratified`
        and an unreadable history are refusals of the same gate and answer
        with the same status; a caller reads which arm it was from the
        message. Pinned because the docstring and the handler comment now
        promise exactly that, and a promise about an exit code that no test
        exercises is the kind that quietly stops being true."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "archive",
                 "change-r", "--yes"],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("not ratified", result.stderr)

    def test_the_archive_subcommand_offers_no_bypass_flag(self):
        """The requirement's own scenario makes accepting a mutation a
        contested-class act requiring an explicit disposition. A flag on this
        gate would be the disposition nobody records, so the subcommand MUST
        NOT grow one."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), ".", "archive", "--help"],
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--yes", result.stdout)
        for flag in ("--force", "--allow-origin-mutation",
                     "--skip-origin-retention", "--no-origin-check"):
            self.assertNotIn(flag, result.stdout)


if __name__ == "__main__":
    unittest.main()
