"""Proposal supporting-document lifecycle tests."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
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
            # AND THE PACKAGE ITSELF, since `install_locked` now INSPECTS the
            # tree it installed rather than believing npm's exit code: a double
            # that left only a `.bin` shim would be exactly the vacuous install
            # `assert_installed_package` exists to refuse.
            installed = prefix / "node_modules" / package
            installed.mkdir(parents=True, exist_ok=True)
            (installed / "package.json").write_text(
                json.dumps({"name": package, "version": version}),
                encoding="utf-8")
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
            # THE ARCHIVE DATE IS TODAY IN UTC AND NOTHING ELSE (#790): since
            # this wrapper asserts that the pinned CLI named
            # `archive/<date>-<change>`, and the CLI names it from its own
            # (now UTC-forced) clock, a literal date here would be a fixture
            # asserting the CLI archived on a day it did not.
            # READ ONCE, NOT THREE TIMES. A run that crossed midnight UTC
            # between the archive and the assertions would compare two
            # different days and fail for the calendar rather than for the
            # code; the wrapper itself derives the date once for exactly this
            # reason, and a fixture that did not would be asserting something
            # weaker than the property under test.
            archive_date = support.utc_today()
            support.archive_change(
                root, "change-a", archive_date, False, True
            )
            archived = list((root / "openspec/changes/archive").glob(
                "????-??-??-change-a"
            ))
            self.assertEqual(len(archived), 1)
            self.assertTrue((archived[0] / "supporting-docs.tar.gz").is_file())
            self.assertEqual(support.verify_archive(archived[0]), [])
            # ONE DATE, TWO PLACES, AND THEY AGREE (#790). The bundle's
            # `packaged_at` and the archive directory's own name are the same
            # UTC day: the wrapper derives it once and asserts the name the
            # pinned CLI produced against it, so a local-clock CLI cannot land
            # a bundle stamped one day beside a directory naming another.
            manifest = (archived[0] / "supporting-docs.manifest.yaml").read_text(
                encoding="utf-8")
            self.assertIn(f'"packaged_at": "{archive_date}"', manifest)
            self.assertTrue(archived[0].name.startswith(f"{archive_date}-"),
                            archived[0].name)
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

            # Today in UTC, read once, for the reason the sibling archive
            # test states.
            archive_date = support.utc_today()
            support.archive_change(root, "change-b", archive_date, False, True)

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
        a crash in the gate rather than a finding from it.

        AND THE REFUSAL ROUTES THE READER (issue #745). It still says there is
        no bypass flag, because there is none; what it no longer does is STOP
        there, which is what it did to the operator on
        codeXfactory/codexFactory #318 who was holding a recorded acceptance.
        Both repairs are named — restore the bytes, or write the record — and
        the record's path and every field it must carry are in the text."""
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
            self.assertIn("RESTORE", result.stderr)
            self.assertIn("openspec/origin-dispositions.yaml", result.stderr)
            for field in support.ORIGIN_DISPOSITION_KEYS:
                self.assertIn(field, result.stderr)

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

    # ----------------------------------------------------------------
    # THE PACKET ITSELF MOVED (issue #833)
    # ----------------------------------------------------------------

    def rename(self, root: Path, old: str, new: str) -> Path:
        """Move a change's directory the way a rename lands: `git mv`, one
        commit, nothing else touched."""
        changes = root / "openspec" / "changes"
        git(root, "mv", str(changes / old), str(changes / new))
        commit_all(root, f"rename {old} to {new}")
        return changes / new

    def assert_walk_refuses(self, root: Path, moved: Path, change: str,
                            named_commit: str,
                            extra_substrings: tuple[str, ...] = ()) -> None:
        """THE SHARED #833 REFUSAL SHAPE. A ratified change renamed
        afterwards and an un-ratifying rename re-ratified later (#849) both
        refuse `ratifying_commit` with the same message shape, stop
        `origin_retention_errors` from returning a findings list, and stop
        `archive_change` itself — the only difference between the two
        callers is WHICH commit the message must name and one #849-only
        substring, so this is that shape asserted once rather than twice."""
        with self.assertRaises(support.OriginRetentionError) as caught:
            support.ratifying_commit(root, change)
        message = str(caught.exception)
        self.assertIn("REFUSE origin-retention-path-moved", message)
        self.assertIn("CANNOT RUN", message)
        self.assertIn(change, message)
        # both paths, so an operator can see WHAT moved WHERE
        self.assertIn("openspec/changes/change-r/proposal.md", message)
        self.assertIn(f"openspec/changes/{change}/proposal.md", message)
        self.assertIn(named_commit[:12], message)
        self.assertIn("FORMER ID", message)
        # …and says WHY it refuses rather than re-basing: the baseline is
        # not merely wrong, it cannot be established at all from history
        self.assertIn("baseline cannot be established", message)
        self.assertIn("#833", message)
        for substring in extra_substrings:
            self.assertIn(substring, message)

        # the refusal is NOT swallowed into a findings list…
        with self.assertRaises(support.OriginRetentionError):
            support.origin_retention_errors(root, moved, change=change)
        # …and the archive itself stops
        with self.assertRaises(support.OriginRetentionError):
            support.archive_change(root, change, "2026-09-05", False, True)

    def test_a_ratified_change_renamed_afterwards_refuses_the_walk(self):
        """THE #833 DEFECT. The walk reads ONE path — the id the tree spells
        today — so a ratified change renamed afterwards has no history under
        its new name before the rename, and the first ratified blob the walk
        finds is the RENAME. That baseline is later than every mutation made
        between the real ratification and it, and the gate printed
        `ORIGIN RETAINED` over exactly that (measured on issue #777).

        THE NEGATIVE CONTROL IS IN THE FIXTURE, so it holds whatever the code
        does: the origin at the rename commit EQUALS the working tree's (a
        baseline taken there finds nothing to report) while the origin at the
        real ratifying commit DIFFERS (there is a mutation to catch). A gate
        that re-based onto the rename would therefore pass this tree, and one
        that refuses cannot pass it by accident.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            ratified_at = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            moved = self.rename(root, "change-r", "change-s")
            renamed_at = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()

            # the negative control, asserted as a property of the history
            here = support.origin_block_lines(
                (moved / ".openspec.yaml").read_text(encoding="utf-8"))
            at_rename = support.origin_block_lines(support.git_show_text(
                root, renamed_at,
                "openspec/changes/change-s/.openspec.yaml"))
            at_ratification = support.origin_block_lines(
                support.git_show_text(
                    root, ratified_at,
                    "openspec/changes/change-r/.openspec.yaml"))
            self.assertEqual(here, at_rename)
            self.assertNotEqual(here, at_ratification)

            # both paths, so an operator can see WHAT moved WHERE, and the
            # walk refuses the #833 shape end to end
            self.assert_walk_refuses(root, moved, "change-s", renamed_at)

    def test_a_ratified_packet_copied_to_a_new_id_refuses_too(self):
        """COPIES COUNT. A "rename" that leaves the old directory standing is
        a duplicated packet rather than a moved one, and the question the
        guard asks — did this packet exist under another name before this
        commit — has the same answer either way. It is also the shape actually
        measured in this corpus: `9ec13c1a` added the new name without
        removing the old one, and git paired it as `C099` rather than `R`.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            copy = root / "openspec" / "changes" / "change-s"
            shutil.copytree(directory, copy)
            commit_all(root, "copy the ratified packet to a second id")
            with self.assertRaises(support.OriginRetentionError) as caught:
                support.ratifying_commit(root, "change-s")
            message = str(caught.exception)
            self.assertIn("origin-retention-path-moved", message)
            # AND THE MESSAGE SAYS WHAT ACTUALLY HAPPENED. Nothing moved
            # here — the old id still stands — so a refusal that spoke only
            # of a MOVE would send an operator looking for a rename that is
            # not in the history (raised by the review bench on PR #846).
            self.assertIn("MOVE OR COPY", message)
            self.assertIn("COPIED", message)
            self.assertTrue(directory.is_dir())
            self.assertIn("openspec/changes/change-r/proposal.md", message)
            self.assertIn("openspec/changes/change-s/proposal.md", message)

    def test_a_ratified_packet_copied_as_a_draft_and_ratified_later_is_not_refused(self):
        """THE FORK-BY-COPY COMPATIBILITY BOUNDARY (Copilot, PR #999). A
        packet newly authored as a COPY of an already-ratified one, entering
        the tree as a DRAFT and ratified only later, is ordinary authoring —
        see `ratified_under_a_former_path`'s "RESTRICTED TO RENAMES" — and
        must stay archivable.

        THE SIBLING COPY TEST ABOVE copies a destination that is ALREADY
        ratified at the copy commit, so it exercises the `kinds="RC"` arm
        `ratifying_commit` takes when the visited commit's own blob declares
        `ratified`, and would still pass even if the OTHER arm — `kinds="R"`,
        taken when it does not — were mistakenly widened back to `"RC"`. This
        fixture copies a DRAFT destination instead, so only the `"R"` arm is
        ever asked at the copy commit; a regression that widens it fails
        here, by refusing a lawful fork-by-copy.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            copy = root / "openspec" / "changes" / "change-t"
            shutil.copytree(directory, copy)
            proposal = copy / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8").replace(
                    "Status: ratified", "Status: draft", 1),
                encoding="utf-8")
            commit_all(root, "copy the ratified packet as a new draft")
            ratify(proposal)
            commit_all(root, "ratify the copied packet under its own history")
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            self.assertEqual(support.ratifying_commit(root, "change-t"), head)
            self.assertEqual(
                support.origin_retention_errors(root, copy,
                                                change="change-t"), [])

    def test_renaming_a_draft_and_ratifying_it_afterwards_is_not_refused(self):
        """RENAMING A DRAFT IS LAWFUL AND STAYS LAWFUL. This corpus does it —
        `46059b77` (#834) renamed a draft change toward the dotless grammar —
        and the flip that follows really is the ratification, so the baseline
        is sound and nothing refuses."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            moved = self.rename(root, "change-r", "change-s")
            ratify(moved / "proposal.md")
            commit_all(root, "record the ratification under the new name")
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            self.assertEqual(support.ratifying_commit(root, "change-s"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-s"), [])

    def test_a_rename_that_also_ratifies_is_itself_the_ratification(self):
        """THE SQUASH SHAPE, and the reason the guard reads the PARENT rather
        than merely noticing a move. A pull request that renames a draft and
        ratifies it lands as ONE commit: the candidate IS a move, and it is
        ALSO the flip — the packet under its former name was still a draft, so
        the baseline is sound and refusing would make such a change
        permanently unarchivable. Every commit in this repository's own
        history arrives squashed, so this is the ordinary case rather than a
        corner."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            changes = root / "openspec" / "changes"
            git(root, "mv", str(changes / "change-r"),
                str(changes / "change-s"))
            moved = changes / "change-s"
            ratify(moved / "proposal.md")
            commit_all(root, "rename the draft and ratify it in one commit")
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            rel = "openspec/changes/change-s/proposal.md"
            # git DOES pair the move at this commit …
            self.assertEqual(
                support.renamed_from(root, head, rel),
                "openspec/changes/change-r/proposal.md")
            # … and the packet was a DRAFT under that name, so nothing refuses
            self.assertIsNone(
                support.ratified_under_a_former_path(root, head, rel))
            self.assertEqual(support.ratifying_commit(root, "change-s"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-s"), [])

    def test_a_change_that_never_moved_is_untouched_by_the_guard(self):
        """The guard's own two answers on the ordinary shape: no predecessor
        pairing at the ratifying commit, and therefore no former path — so the
        walk returns the flip it always returned."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            rel = "openspec/changes/change-r/proposal.md"
            self.assertIsNone(support.renamed_from(root, head, rel))
            self.assertIsNone(
                support.ratified_under_a_former_path(root, head, rel))
            self.assertEqual(support.ratifying_commit(root, "change-r"), head)
            # end to end, not only at the walk: the gate still passes it
            self.assertEqual(
                support.origin_retention_errors(
                    root, root / "openspec" / "changes" / "change-r"), [])

    def test_a_never_ratified_change_that_moved_is_still_not_ratified(self):
        """THE DRAFT ARM IS NOT HIJACKED. A change that was never ratified has
        no baseline to establish and no ratification to have moved away from,
        so it takes the `not ratified` finding it always took — not the moved
        packet refusal."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            moved = self.rename(root, "change-r", "change-s")
            self.assertIsNone(support.ratifying_commit(root, "change-s"))
            self.assertIn(
                "not ratified",
                "\n".join(support.origin_retention_errors(
                    root, moved, change="change-s")))

    def test_the_cli_refuses_a_moved_packet_with_exit_2_and_no_traceback(self):
        """The fourth arm answers with the gate's own status, like the other
        three: 2, the named code on stderr, and no stack trace — a traceback
        here would read as a crash in the gate rather than a refusal from
        it."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            self.rename(root, "change-r", "change-s")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "archive",
                 "change-s", "--yes"],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("origin-retention-path-moved", result.stderr)

    def test_an_unratifying_rename_now_refuses_the_walk(self):
        """THE #849 GAP, CLOSED FOR RENAMES (Codex's P1 on PR #846). The
        guard used to ask its question only of the commit that ends up
        declaring `ratified`, so a commit that renames an already-ratified
        packet AND un-ratifies the destination in the same commit was never
        asked, and a LATER commit re-ratifying it — which carries no rename
        pairing of its own — was taken as the baseline instead: later than
        the real ratification, with the mutation this fixture puts in
        between waved through, which was #833's failure by a longer route.

        `ratifying_commit` now asks EVERY commit it visits, not only the one
        whose own blob declares `ratified`, so the rename-and-un-ratify
        commit answers the question before the re-ratification is ever
        reached, and refuses there instead — naming the RENAME commit, not
        the pairing-free re-ratification a caller might otherwise suspect.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(changes / "change-r"),
                str(changes / "change-s"))
            moved = changes / "change-s"
            proposal = moved / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8").replace(
                    "Status: ratified", "Status: draft", 1),
                encoding="utf-8")
            commit_all(root, "rename the ratified packet and un-ratify it")
            renamed_at = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            ratify(proposal)
            commit_all(root, "re-ratify it under the new name")

            # the RENAME is named, not the pairing-free re-ratification, and
            # the walk refuses the #833 shape plus the #849 substring too
            self.assert_walk_refuses(root, moved, "change-s", renamed_at,
                                     extra_substrings=("#849",))

    # ----------------------------------------------------------------
    # THE RENAME CHAIN (issue #1003)
    # ----------------------------------------------------------------

    def rename_and_un_ratify(self, root: Path, old: str, new: str) -> Path:
        """The #849 hop as ONE commit: `git mv`, and the destination's own
        header flipped back to `draft` before anything is committed. Its own
        blob is therefore NOT ratified, which is what kept it out of the
        walk's question until #999."""
        changes = root / "openspec" / "changes"
        git(root, "mv", str(changes / old), str(changes / new))
        moved = changes / new
        proposal = moved / "proposal.md"
        proposal.write_text(
            proposal.read_text(encoding="utf-8").replace(
                "Status: ratified", "Status: draft", 1),
            encoding="utf-8")
        commit_all(root, f"rename {old} to {new} and un-ratify it")
        return moved

    def test_a_rename_chain_refuses_at_the_hop_that_moved_the_ratified_packet(self):
        """THE #1003 SHAPE, routed from the review bench on PR #999. #849
        closed the un-ratifying rename at ONE hop, and the walk that closed
        it still enumerates commits with a plain path-limited `git log` for
        the name the tree spells TODAY — which follows no rename at all. One
        more hop therefore walked straight past it: after `ratify r →
        rename+un-ratify r→s → rename s→t while draft → ratify t`, the
        commits that touched `change-t` BEGIN at the `s→t` rename, whose
        former blob is a draft and refuses nothing, and the later
        re-ratification was taken as the baseline — #833's failure and
        #849's, reached by one hop more than either closed.

        THE NEGATIVE CONTROL IS IN THE FIXTURE, as it is for #833 above, so
        it holds whatever the code does: the origin at the re-ratification
        EQUALS the working tree's (a baseline taken there finds nothing to
        report) while the origin at the real ratification DIFFERS. A walk
        that re-based onto the chain's end passes this tree; one that
        refuses cannot pass it by accident.

        AND THE COMMIT NAMED IS THE HOP THAT MOVED THE RATIFIED PACKET — the
        `r→s` rename — not the `s→t` hop that carried a draft onward, and not
        the pairing-free re-ratification a caller might otherwise suspect.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            ratified_at = self.sha(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            self.rename_and_un_ratify(root, "change-r", "change-s")
            moved_at = self.sha(root)
            moved = self.rename(root, "change-s", "change-t")
            ratify(moved / "proposal.md")
            commit_all(root, "re-ratify it under its third name")
            re_ratified_at = self.sha(root)

            # the negative control, asserted as a property of the history
            here = support.origin_block_lines(
                (moved / ".openspec.yaml").read_text(encoding="utf-8"))
            at_re_ratification = support.origin_block_lines(
                support.git_show_text(
                    root, re_ratified_at,
                    "openspec/changes/change-t/.openspec.yaml"))
            at_ratification = support.origin_block_lines(
                support.git_show_text(
                    root, ratified_at,
                    "openspec/changes/change-r/.openspec.yaml"))
            self.assertEqual(here, at_re_ratification)
            self.assertNotEqual(here, at_ratification)

            # the FIRST hop is named, and the message carries all three
            # names: the path the packet was ratified under, the path it was
            # moved to at that commit, and the one it occupies today
            self.assert_walk_refuses(
                root, moved, "change-t", moved_at,
                extra_substrings=("#1003",
                                  "openspec/changes/change-s/proposal.md"))

    def test_a_three_hop_rename_chain_still_refuses_at_the_first_hop(self):
        """HOP COUNT IS NOT A PROPERTY OF THE DEFECT. Nothing in the walk
        should care how many lawful draft renames stand between the move and
        the name the tree spells today, so this adds a third hop to the
        fixture above and asserts the same refusal naming the same commit."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            self.rename_and_un_ratify(root, "change-r", "change-s")
            moved_at = self.sha(root)
            self.rename(root, "change-s", "change-t")
            moved = self.rename(root, "change-t", "change-u")
            ratify(moved / "proposal.md")
            commit_all(root, "re-ratify it under its fourth name")
            self.assert_walk_refuses(
                root, moved, "change-u", moved_at,
                extra_substrings=("#1003",
                                  "openspec/changes/change-s/proposal.md"))

    def test_a_draft_renamed_twice_and_ratified_at_the_end_still_archives(self):
        """RENAMING A DRAFT STAYS LAWFUL, HOWEVER OFTEN IT HAPPENS. This
        corpus renames drafts (`46059b77`, #834); doing it twice before the
        ratification is that same lawful act twice, and a walk that follows
        the lineage must not turn a longer lawful history into a refusal —
        which is exactly the trap a hop-chain guard refusing on ANY hop
        would fall into (`ratified_under_a_former_path`, "RESTRICTED TO
        RENAMES"), this gate having no bypass flag by design (#690)."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            self.rename(root, "change-r", "change-s")
            moved = self.rename(root, "change-s", "change-t")
            ratify(moved / "proposal.md")
            commit_all(root, "record the ratification under the third name")
            head = self.sha(root)
            self.assertEqual(support.ratifying_commit(root, "change-t"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-t"), [])

    def test_a_ratified_packet_renamed_twice_refuses_at_the_first_hop(self):
        """A CHAIN CARRYING NO UN-RATIFICATION AT ALL still refuses, because
        renaming a RATIFIED change is blocked outright until a change
        declares a former id (#833; `docs/document-lifecycle.md` § "Gates In
        Practice": "Renaming a ratified change is therefore blocked until a
        change declares a FORMER ID").

        WHAT THE LINEAGE WALK MOVES HERE IS WHICH COMMIT THE REFUSAL NAMES.
        The single-path walk saw only the LAST hop — the one commit that
        touched the name the tree spells today — and named it; the lineage
        walk reaches the FIRST hop, where the ratified packet actually left
        the name it was ratified under, and names that instead. Both refuse;
        the earlier commit is the one an operator can act on."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            self.rename(root, "change-r", "change-s")
            moved_at = self.sha(root)
            moved = self.rename(root, "change-s", "change-t")
            self.assert_walk_refuses(
                root, moved, "change-t", moved_at,
                extra_substrings=("#1003",
                                  "openspec/changes/change-s/proposal.md"))

    def test_a_draft_fork_by_copy_renamed_afterwards_still_archives(self):
        """THE FORK-BY-COPY BOUNDARY SURVIVES THE CHAIN. A predecessor is
        followed as a RENAME only (`kinds="R"`), never as a copy, so a packet
        authored as a draft COPY of a ratified one — and renamed afterwards
        while still a draft — is ordinary authoring and stays archivable. A
        lineage walk that followed the copy hop backwards would land in the
        SOURCE packet's ratified history and refuse a lawful fork
        permanently, this gate having no bypass flag (#690). The sibling
        single-hop fixture above pins the same boundary at one hop; this one
        pins it after the lineage walk has a hop to follow."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            copy = root / "openspec" / "changes" / "change-t"
            shutil.copytree(directory, copy)
            proposal = copy / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8").replace(
                    "Status: ratified", "Status: draft", 1),
                encoding="utf-8")
            commit_all(root, "copy the ratified packet as a new draft")
            moved = self.rename(root, "change-t", "change-u")
            ratify(moved / "proposal.md")
            commit_all(root, "ratify the forked packet under its own name")
            head = self.sha(root)
            self.assertTrue(directory.is_dir())
            self.assertEqual(support.ratifying_commit(root, "change-u"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-u"), [])

    def test_an_un_ratification_before_the_rename_is_a_stated_gap(self):
        """A STATED GAP, PINNED RATHER THAN CLOSED — the precedent being
        #846's own `test_an_unratifying_rename_escapes_the_guard_a_stated_gap`,
        which pinned #849's shape with a fixture until #999 closed it.

        Where the un-ratification is its OWN commit and the rename comes
        later, every hop in the lineage moved a DRAFT, so no hop moved an
        already-ratified packet and nothing refuses: the baseline is the
        later re-ratification, exactly as it was before #1003. Closing this
        one turns on whether a re-ratification after a return to draft is
        lawfully a NEW baseline — a governance question rather than an
        author's — and #1003 names the shape whose un-ratification rides IN
        the rename commit rather than this one. So today's answer is pinned
        here and left where it is, and a later change that means to move it
        has to move this fixture and say so."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            proposal = directory / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8").replace(
                    "Status: ratified", "Status: draft", 1),
                encoding="utf-8")
            commit_all(root, "return the ratified packet to draft")
            moved = self.rename(root, "change-r", "change-s")
            ratify(moved / "proposal.md")
            commit_all(root, "re-ratify it under the new name")
            head = self.sha(root)
            self.assertEqual(support.ratifying_commit(root, "change-s"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-s"), [])

    # ----------------------------------------------------------------
    # WHAT THE LINEAGE WALK MUST NOT DO (review bench, PR #1024)
    # ----------------------------------------------------------------

    def test_a_reused_intermediate_name_does_not_contaminate_a_later_packet(self):
        """A PATH IS NOT AN IDENTITY. An old ratified `r` is renamed to `s`;
        `s` is renamed onward to `u`, so that name falls vacant; a NEW and
        unrelated draft is then authored at `s` and renamed to `t` before
        being ratified. The name `s` therefore carries two packets' histories,
        and a lineage walk that read the WHOLE history of that name would
        refuse `t` for a move that belonged to somebody else — permanently,
        this gate having no bypass flag (#690). The predecessor history is
        trimmed to the incarnation the hop actually renamed away, so `t`
        archives on its own history.

        THE ANTI-VACUITY HALF IS IN THE SAME FIXTURE: the OLD packet, which
        really was renamed while ratified, still refuses. A walk that trimmed
        too far would pass both, and this tree tells the two apart."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            self.rename(root, "change-r", "change-s")
            self.rename(root, "change-s", "change-u")
            fresh = root / "openspec" / "changes" / "change-s"
            fresh.mkdir(parents=True)
            (fresh / "proposal.md").write_text(
                "---\nStatus: draft\n---\n\n## Why\n\nA different packet, "
                "authored at a name that fell vacant.\n", encoding="utf-8")
            (fresh / "tasks.md").write_text(
                "## 1. Work\n\n- [x] 1.1 Done\n", encoding="utf-8")
            (fresh / ".openspec.yaml").write_text(
                "schema: spec-driven\ncreated: 2026-09-06\n"
                "origin:\n  kind: ad_hoc\n"
                "  id: fixture:adhoc:2026-09-06-change-t\n"
                "  reason: a second fixture packet, unrelated to the first\n"
                "  approved_by: >-\n    Fixture Authority, for the second "
                "packet\n  approved_on: '2026-09-06'\n", encoding="utf-8")
            commit_all(root, "author a new draft at the vacant name")
            moved = self.rename(root, "change-s", "change-t")
            ratify(moved / "proposal.md")
            commit_all(root, "ratify the new packet under its own name")
            head = self.sha(root)

            self.assertEqual(support.ratifying_commit(root, "change-t"), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change="change-t"), [])
            # …and the packet that really did move while ratified still refuses
            with self.assertRaises(support.OriginRetentionError):
                support.ratifying_commit(root, "change-u")

    def test_a_rename_that_landed_through_a_merge_still_refuses(self):
        """MERGE PARENTS, MEASURED RATHER THAN FEARED. A branch ratifies `r`
        and renames it to `s` while the first-parent side of the merge still
        carries a DRAFT `r`, and the branch lands as a merge commit. git
        reports NO rename pairing at the merge itself — `git log --follow -1
        <merge> -- <path>` answers with the BRANCH's own rename commit, and
        `renamed_from` accepts a pairing only where git's `%H` is the revision
        asked about — so the question is put to the branch commit that made
        the move, where the parent read is exact, and the walk refuses there
        rather than reading the first parent's draft and passing.

        The predecessor bound is every parent of a hop for the same reason
        (`_parents`), so a lineage that DID run through a merge would be read
        from both sides rather than from the first."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            trunk = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
                check=True, capture_output=True,
                text=True).stdout.strip()
            git(root, "checkout", "-q", "-b", "feature")
            changes = root / "openspec" / "changes"
            ratify(changes / "change-r" / "proposal.md")
            commit_all(root, "ratify the packet on the branch")
            moved = self.rename(root, "change-r", "change-s")
            renamed_at = self.sha(root)
            git(root, "checkout", "-q", trunk)
            (root / "README.md").write_text("the trunk moved on\n",
                                            encoding="utf-8")
            commit_all(root, "an unrelated commit on the trunk")
            git(root, "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "merge", "--no-ff", "-q",
                "-m", "merge the branch that renamed the ratified packet",
                "feature")
            merged_at = self.sha(root)

            # the merge itself carries no pairing — the property the refusal
            # below rests on, asserted rather than assumed
            rel = "openspec/changes/change-s/proposal.md"
            self.assertIsNone(support.renamed_from(root, merged_at, rel))
            self.assertEqual(support.renamed_from(root, renamed_at, rel),
                             "openspec/changes/change-r/proposal.md")
            self.assert_walk_refuses(root, moved, "change-s", renamed_at)

    def test_a_lineage_git_will_not_read_refuses_rather_than_reading_a_silence(self):
        """A CHECK THAT CANNOT RUN MUST NOT PASS — at the lineage too. A
        bounded `git log` that FAILS is not a history that is empty, and
        reading the one as the other would switch this guard off exactly
        where it is meant to bite: in a checkout whose history is not all
        there.

        BOTH LAYERS ARE MEASURED HERE, AND BOTH REFUSE AS WHAT THEY ARE. The
        walk's own arm refuses when a bound cannot be read, and a repository
        with a hop's parent commit object DELETED — which reaches the CURRENT
        name's enumeration as well — refuses END TO END on the same arm. That
        second half took two rounds: the first answer left the current name's
        `git log` reading its own failure as an empty history, which still
        refused, but on the `not ratified` arm — a refusal that tells an
        operator to go and commit a ratification already sitting in the
        history they could not read (PR #1024's bench, second round). A
        refusal must name what actually happened, so both now answer
        `origin-retention-history-unreadable` and say which read failed."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            self.rename_and_un_ratify(root, "change-r", "change-s")
            hop = self.sha(root)
            parent = self.sha(root, f"{hop}^")
            moved = self.rename(root, "change-s", "change-t")
            ratify(moved / "proposal.md")
            commit_all(root, "re-ratify it under its third name")

            # the arm itself: a bound git cannot resolve is CANNOT RUN
            with self.assertRaises(support.OriginRetentionError) as caught:
                support._incarnation(root, "change-t",
                                     "openspec/changes/change-s/proposal.md",
                                     "no-such-revision")
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            self.assertIn("CANNOT RUN", str(caught.exception))

            # and end to end, with the object actually gone
            (root / ".git" / "objects" / parent[:2] / parent[2:]).unlink()
            with self.assertRaises(support.OriginRetentionError) as caught:
                support.origin_retention_errors(root, moved,
                                                change="change-t")
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            # the refusal NAMES the read that failed rather than saying only
            # that something did — this one is the current name's own
            # enumeration, which is what the first round left generic
            self.assertIn("It needed the history of "
                          "`openspec/changes/change-t/proposal.md`",
                          str(caught.exception))
            self.assertNotIn("not ratified", str(caught.exception))
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(root, "change-t", "2026-09-05",
                                       False, True)

    # ----------------------------------------------------------------
    # A PARTIAL CHECKOUT MUST NOT BE A PASS (review bench, PR #1024,
    # second round)
    #
    # `git_show_text` and `renamed_from` each answered ABSENT and UNREADABLE
    # with one value, and the walk read both as clean answers: no ratified
    # predecessor, no predecessor at all, nothing earlier under that name.
    # The checkout that makes every one of those a lie is not exotic — a
    # `--filter=blob:none` clone whose promisor is unreachable lists the
    # predecessor's `proposal.md` in its tree and cannot read the blob
    # behind it. Both fixtures below are that clone, and both are measured
    # against the FULL clone of the same history, where the walk refuses.
    #
    # WHAT THE PARTIAL CLONE DID BEFORE THIS ROUND DIFFERS BETWEEN THEM,
    # and the difference is why the first pins `_incarnation` directly
    # rather than through an outcome (measured against `a90e6ccd`, both).
    # On the #1003 chain — the hop whose pairing cannot be read — the walk
    # RETURNED a baseline and printed `ORIGIN RETAINED` over a mutated
    # origin. On the byte-exact chain a sibling arm still refused, but it
    # named the LAST hop where the full clone names the FIRST: the lineage
    # trimmed at a tree it could not read, and a guard that has silently
    # stopped seeing the shape it was widened for is one round away from
    # the same pass.
    # ----------------------------------------------------------------

    def a_lineage_with_a_mutated_origin(self, root: Path) -> dict:
        """The opening every fixture below shares: a packet ratified under
        `change-r`, its origin mutated afterwards — so a baseline resolved
        anywhere later waves the mutation through — and a paragraph written
        under that first name.

        THE PARAGRAPH IS THE FIXTURE'S MECHANISM, not decoration. A blob is
        unreadable in a partial checkout only where its CONTENT is not also
        at HEAD, and a packet this small would otherwise carry the same bytes
        at both ends of its own chain.
        """
        directory = self.packet(root)
        hops = {"created": self.sha(root, "HEAD~1"),
                "ratified": self.sha(root)}
        proposal = directory / "proposal.md"
        proposal.write_text(
            proposal.read_text(encoding="utf-8")
            + "\nThe first name's own paragraph.\n", encoding="utf-8")
        commit_all(root, "write under the name it was ratified with")
        self.mutate(directory, "quoting the ratified prose",
                    "quoting the corrected prose")
        commit_all(root, "mutate the origin after ratification")
        return hops

    def a_moved_ratified_lineage(self, root: Path) -> dict:
        """`ratify r → git mv r→s → edit s → git mv s→t`, every hop
        BYTE-EXACT — which is the knob that decides what a partial checkout
        can still do: git pairs an exact rename from object ids alone, so the
        pairings all survive and the BLOB reads are what fail."""
        hops = self.a_lineage_with_a_mutated_origin(root)
        moved = self.rename(root, "change-r", "change-s")
        hops["r_to_s"] = self.sha(root)
        proposal = moved / "proposal.md"
        proposal.write_text(
            proposal.read_text(encoding="utf-8")
            + "An edit while it sat at its second name.\n", encoding="utf-8")
        commit_all(root, "edit it under its second name")
        hops["moved"] = self.rename(root, "change-s", "change-t")
        hops["s_to_t"] = self.sha(root)
        return hops

    def an_un_ratifying_lineage(self, root: Path) -> dict:
        """The #1003 chain — `ratify r → rename+un-ratify r→s → rename s→t
        AMENDING it → ratify t` — whose second hop is INEXACT, because the
        commit that moved the packet also added a line to it. That is the hop
        a partial checkout cannot pair at all."""
        hops = self.a_lineage_with_a_mutated_origin(root)
        self.rename_and_un_ratify(root, "change-r", "change-s")
        hops["r_to_s"] = self.sha(root)
        changes = root / "openspec" / "changes"
        git(root, "mv", str(changes / "change-s"), str(changes / "change-t"))
        moved = changes / "change-t"
        proposal = moved / "proposal.md"
        proposal.write_text(
            proposal.read_text(encoding="utf-8")
            + "A line added as the packet moved.\n", encoding="utf-8")
        commit_all(root, "rename change-s to change-t, amending it")
        hops["s_to_t"] = self.sha(root)
        ratify(proposal)
        commit_all(root, "re-ratify it under its third name")
        hops["moved"] = moved
        return hops

    def partial_checkout(self, source: Path, destination: Path,
                         unreadable: tuple[str, str]) -> Path:
        """A `--filter=blob:none` clone of `source` with its promisor cut.

        The blobs the working tree needs are fetched while the promisor is
        still reachable, so HEAD reads normally and HISTORY does not: a blob
        whose content differs from anything at HEAD was never fetched and can
        no longer be. `unreadable` is the (revision, path) each fixture rests
        on, and it is PROVED rather than assumed — a git that ignored the
        filter would otherwise turn these fixtures green by being unable to
        pose the question at all."""
        git(source, "config", "uploadpack.allowFilter", "true")
        subprocess.run(
            ["git", "clone", "-q", "--filter=blob:none", f"file://{source}",
             str(destination)], check=True, capture_output=True, text=True)
        git(destination, "remote", "set-url", "origin",
            f"file://{source.parent / 'no-such-promisor'}")
        revision, rel = unreadable
        probe = subprocess.run(
            ["git", "-C", str(destination), "show", f"{revision}:{rel}"],
            capture_output=True, text=True)
        if probe.returncode == 0:
            self.skipTest("this git did not honour --filter=blob:none over "
                          "file://, so there is no unreadable blob to test")
        # THE TREE STILL LISTS IT: presence and readability are two questions,
        # and the whole finding is that one value was answering both
        self.assertIs(support._path_present(destination, revision, rel), True)
        self.assertIsNone(support.git_show_text(destination, revision, rel))
        return destination

    def assert_the_full_clone_refuses(self, root: Path, change: str,
                                      hops: dict) -> None:
        """ANTI-VACUITY FOR BOTH FIXTURES BELOW. A partial checkout is only
        interesting where the SAME history refuses once it can all be read —
        a fixture git could not pair at all would make a fail-closed walk and
        a blind one agree, and the test would pass either way."""
        with self.assertRaises(support.OriginRetentionError) as caught:
            support.ratifying_commit(root, change)
        self.assertIn("origin-retention-path-moved", str(caught.exception))
        self.assertIn(hops["r_to_s"][:12], str(caught.exception))

    def test_a_partial_checkout_that_cannot_read_the_predecessor_refuses(self):
        """AN UNREADABLE BLOB IS NOT AN ABSENT ONE. `git_show_text` answers
        both with None, and the walk asked it two questions that turn on the
        difference: where an earlier incarnation of a name CAME INTO BEING
        (its boundary), and what the packet declared at a commit. Here the
        true answers are "it stood there" and "this is what it said"; the
        flattened ones are "it did not" and "nothing".

        MEASURED, against the same history fully readable: `_incarnation`
        kept ONE commit where the full checkout keeps two — the hop that
        moved the ratified packet trimmed out of the lineage altogether. What
        that costs is not visible in every shape, and it is not in this one:
        a sibling arm still refuses here, because the same hop is asked again
        under the current name. So the trim is pinned DIRECTLY rather than
        through an outcome — a lineage that silently loses hops is a guard
        that has stopped being able to see the shape it was widened for, and
        the next fixture is the shape where nothing else catches it.

        THE END-TO-END HALF IS THE REASON, not the refusal: the walk now
        answers `origin-retention-history-unreadable` naming the blob it
        could not read, rather than whatever it stumbles into afterwards."""
        with TemporaryDirectory() as td:
            root = Path(td) / "full"
            root.mkdir(parents=True)
            hops = self.a_moved_ratified_lineage(root)
            self.assert_the_full_clone_refuses(root, "change-t", hops)
            r_rel = "openspec/changes/change-r/proposal.md"
            s_rel = "openspec/changes/change-s/proposal.md"
            clone = self.partial_checkout(root, Path(td) / "partial",
                                          (hops["created"], r_rel))

            # THE BOUNDARY, which is the read the finding names: the hop that
            # moved the ratified packet is still in the incarnation, because
            # "the name stood in no parent" is read off the TREE
            self.assertEqual(
                support._incarnation(clone, "change-t", s_rel,
                                     hops["s_to_t"]),
                support._incarnation(root, "change-t", s_rel,
                                     hops["s_to_t"]))
            self.assertIn(hops["r_to_s"],
                          support._incarnation(clone, "change-t", s_rel,
                                               hops["s_to_t"]))

            # and the walk refuses rather than resolving a late baseline
            with self.assertRaises(support.OriginRetentionError) as caught:
                support.ratifying_commit(clone, "change-t")
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            self.assertIn(f"the blob `{r_rel}` stands as at "
                          f"{hops['created'][:12]}", str(caught.exception))
            moved = clone / "openspec" / "changes" / "change-t"
            with self.assertRaises(support.OriginRetentionError):
                support.origin_retention_errors(clone, moved,
                                                change="change-t")
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(clone, "change-t", "2026-09-05",
                                       False, True)

    def test_a_partial_checkout_that_cannot_read_the_pairing_refuses(self):
        """AND A `--follow` GIT COULD NOT RUN IS NOT "THIS WAS NEVER
        RENAMED". Rename detection reads blobs wherever the move was not
        byte-exact, so a hop that AMENDED the packet as it moved is precisely
        the hop a partial checkout cannot pair — and `renamed_from` reports
        that failure as None, the value it already uses for "no predecessor".
        Read flat, the lineage simply ENDS there, and everything behind the
        hop, the real ratification included, is never asked about.

        MEASURED against the full clone of the same history, where the
        pairing IS reported and the walk refuses: in the partial checkout
        `renamed_from` answers None at that very hop, and the walk used to
        answer `ORIGIN RETAINED` over a mutated origin."""
        with TemporaryDirectory() as td:
            root = Path(td) / "full"
            root.mkdir(parents=True)
            hops = self.an_un_ratifying_lineage(root)
            self.assert_the_full_clone_refuses(root, "change-t", hops)
            t_rel = "openspec/changes/change-t/proposal.md"
            s_rel = "openspec/changes/change-s/proposal.md"
            clone = self.partial_checkout(root, Path(td) / "partial",
                                          (hops["r_to_s"], s_rel))

            # the pairing the full clone reports is the one this checkout
            # cannot read — and the FLAT reading calls that "no predecessor"
            self.assertEqual(
                support.renamed_from(root, hops["s_to_t"], t_rel), s_rel)
            self.assertIsNone(
                support.renamed_from(clone, hops["s_to_t"], t_rel))

            with self.assertRaises(support.OriginRetentionError) as caught:
                support.ratifying_commit(clone, "change-t")
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            self.assertIn(f"whether {hops['s_to_t'][:12]} renamed "
                          f"`{t_rel}` in from an earlier name",
                          str(caught.exception))
            moved = clone / "openspec" / "changes" / "change-t"
            with self.assertRaises(support.OriginRetentionError):
                support.origin_retention_errors(clone, moved,
                                                change="change-t")
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(clone, "change-t", "2026-09-05",
                                       False, True)

    def test_a_long_lawful_draft_rename_chain_is_not_capped(self):
        """NO ARBITRARY DEPTH. "Renaming a DRAFT change is unaffected" carries
        no number, so neither does the walk: it follows the lineage
        iteratively, bounded by the history itself rather than by a constant,
        and a packet renamed seventy times while still a draft archives on
        the ratification it finally got. A depth cap here would have been a
        refusal nobody ruled, on a gate with no bypass flag (#690)."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root, ratified=False)
            changes = root / "openspec" / "changes"
            current = "change-r"
            for step in range(70):
                following = f"change-{step:03d}"
                git(root, "mv", str(changes / current),
                    str(changes / following))
                commit_all(root, f"rename {current} to {following}")
                current = following
            moved = changes / current
            ratify(moved / "proposal.md")
            commit_all(root, "ratify it under the name it ended up with")
            head = self.sha(root)
            self.assertEqual(support.ratifying_commit(root, current), head)
            self.assertEqual(
                support.origin_retention_errors(root, moved,
                                                change=current), [])

    def test_the_guard_reads_any_spelling_of_the_candidate_commit(self):
        """A REVISION IS A REVISION, however it is spelled — and getting that
        wrong is silent NON-detection, which is the failure class this whole
        guard exists to end rather than a cosmetic defect. The pairing is
        recognised by matching git's own `%H` against the revision asked
        about, so a caller naming the commit any other lawful way (`HEAD`, an
        abbreviated hash, an annotated tag) would have compared unequal, been
        answered None, and let the walk re-base onto the move exactly as it
        did before #833. Raised by the review bench on PR #846; the only
        caller today passes a full hash out of `git log --format=%H`, so this
        pins the property rather than repairing a live failure."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            self.rename(root, "change-r", "change-s")
            head = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True, capture_output=True, text=True).stdout.strip()
            git(root, "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "tag", "-a", "-m",
                "the move", "the-move")
            rel = "openspec/changes/change-s/proposal.md"
            former = "openspec/changes/change-r/proposal.md"
            for spelling in (head, head[:12], "HEAD", "the-move"):
                with self.subTest(revision=spelling):
                    self.assertEqual(
                        support.renamed_from(root, spelling, rel), former)
                    self.assertEqual(
                        support.ratified_under_a_former_path(
                            root, spelling, rel), former)
            # A REVISION THAT RESOLVES TO NOTHING SPLITS THE TWO READINGS,
            # which is the contract PR #1024's bench asked for: the FLAT one
            # still answers None — "no predecessor was named" — while the
            # guard's own reading refuses, because git declining to resolve a
            # revision is not evidence that nothing was renamed there.
            self.assertIsNone(
                support.renamed_from(root, "no-such-revision", rel))
            self.assertIsNone(
                support._pairing_at(root, "no-such-revision", rel,
                                    kinds="RC"))
            self.assertEqual(
                support._pairing_at(root, head, rel, kinds="RC"), former)
            with self.assertRaises(support.OriginRetentionError) as caught:
                support.ratified_under_a_former_path(
                    root, "no-such-revision", rel)
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            # and it names the packet even though the caller named a path
            self.assertIn("change-s:", str(caught.exception))

    def test_a_git_config_cannot_switch_the_guard_off(self):
        """NO GIT CONFIG SWITCHES THE GUARD OFF. Rename detection is
        configurable — `diff.renames=false`, `diff.renameLimit=1` — and a
        guard that read the pairing from a plain diff could be turned off,
        with the #833 defect back, from outside the repository's own rules.
        The gate's arms are not configurable by design (#690: no bypass
        flag), so neither is this one: `--follow` FORCES detection, which is
        the mechanism rather than the explicit `--find-renames` beside it
        (dropping that flag breaks nothing — measured). So this asserts the
        PROPERTY over the hostile config, set in the fixture's own
        `.git/config`, and not the flag."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self.packet(root)
            git(root, "config", "diff.renames", "false")
            git(root, "config", "diff.renameLimit", "1")
            self.rename(root, "change-r", "change-s")
            with self.assertRaisesRegex(support.OriginRetentionError,
                                        "origin-retention-path-moved"):
                support.ratifying_commit(root, "change-s")

    @unittest.skipUnless((REPO_ROOT / ".git").exists(),
                         "no git history for this checkout")
    def test_the_guard_refuses_nothing_on_this_repository_today(self):
        """THE GUARD IS A NO-OP ON THE LAWFUL CORPUS, measured rather than
        asserted: every active change resolves the baseline it resolved
        before the guard existed. NO COUNT IS WRITTEN DOWN, because the
        corpus gains and loses packets with every landing and a number here
        is stale by the next one — the invariant is zero refusals over
        WHATEVER is active, one subtest per change, and the same sweep run by
        hand over the active AND archived packets (comparing each resolved
        baseline against the pre-guard module's) found zero refusals and zero
        baselines moved. A refusal appearing here means a ratified change has
        been renamed — which is the act this gate exists to stop, not a
        defect in it."""
        active = REPO_ROOT / "openspec" / "changes"
        resolved = []
        for directory in sorted(active.iterdir()):
            if not directory.is_dir() or directory.name == "archive":
                continue
            with self.subTest(change=directory.name):
                resolved.append(
                    support.ratifying_commit(REPO_ROOT, directory.name))
        # ANTI-VACUITY, both halves: the sweep saw changes at all, and it saw
        # RATIFIED ones — a corpus of drafts alone would never reach the
        # guard, and "nothing refused" would then mean "nothing was asked".
        self.assertTrue(resolved)
        self.assertTrue([sha for sha in resolved if sha is not None])

    # ----------------------------------------------------------------
    # THE EXPLICIT DISPOSITION THE REQUIREMENT PROMISES (issue #745)
    #
    # `release-realization` § "Origin retention at archive" ends its mutation
    # scenario with "restoring or accepting the mutation is a contested-class
    # act requiring an explicit disposition". Until the record below existed,
    # the gate could read the RESTORING half and nothing else: an owner's
    # ACCEPTED mutation and an unnoticed edit produced the identical refusal.
    # Measured rather than argued — codeXfactory/codexFactory #318 recorded
    # Brett Heap's "accept the mutation, this lane re-runs the archives" over
    # `add-floor-regeneration-automation` (ratifying commit ec286270b10f,
    # mutating commit 76758a1b, `changed keys: approved_by`, a tense-only
    # rewording fourteen minutes later in the same pull request) and the
    # re-run refused byte-identically.
    #
    # EVERY CONTROL BELOW MEASURES. The record is written into a real tree,
    # the commits it names are real commits in a real history, and each
    # assertion is on what the gate DOES — the archive proceeding, or refusing
    # while naming what did not match — rather than on what its prose says it
    # will do.
    # ----------------------------------------------------------------

    WORD = "accept the mutation, this lane re-runs the archives"
    CITED_TO = ("https://github.com/codeXfactory/codexFactory/issues/232"
                "#issuecomment-5610686281")

    def sha(self, root: Path, revision: str = "HEAD") -> str:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", revision],
            check=True, capture_output=True, text=True).stdout.strip()

    def record_text(self, *entries: dict, schema_version: object = 1,
                    kind: str = "origin_dispositions") -> str:
        """The record AS AN OPERATOR WRITES IT — literal YAML, so these tests
        pin the ON-DISK SHAPE rather than a dumper's opinion of it, and every
        entry scalar is quoted (the rule
        `tests/sequenced_after/archive-date-dispositions.yaml` settled on)."""
        rows = [f"schema_version: {schema_version}", f"kind: {kind}", "",
                "dispositions:"]
        for entry in entries:
            first = True
            for key, value in entry.items():
                if isinstance(value, list):
                    rendered = "[" + ", ".join(f'"{item}"'
                                               for item in value) + "]"
                elif isinstance(value, str):
                    rendered = '"' + value.replace('"', '\\"') + '"'
                else:  # a deliberately UNQUOTED scalar, for the trap test
                    rendered = str(value)
                rows.append(("  - " if first else "    ")
                            + f"{key}: {rendered}")
                first = False
        return "\n".join(rows) + "\n"

    def write_record(self, root: Path, *entries: dict, text: str | None = None,
                     rel: str = "openspec/origin-dispositions.yaml",
                     **header) -> Path:
        path = root.joinpath(*rel.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.record_text(*entries, **header) if text is None else text,
            encoding="utf-8")
        return path

    def accept_entry(self, change: str, ratified_at: str, mutation_at: str,
                     changed_keys: tuple = ("approved_by",),
                     **overrides) -> dict:
        """A VALID entry, and the one thing each negative control changes.

        A value of `None` passed through `**overrides` DELETES that key; a
        key this builder takes as a named parameter is removed with `pop`
        instead (the missing-field control below)."""
        entry = {
            "change_id": change,
            "ratified_at": ratified_at,
            "mutation_at": mutation_at,
            "changed_keys": list(changed_keys),
            "disposition": "accept",
            "disposed_by": "Brett Heap",
            "disposed_on": "2026-09-10",
            "word": self.WORD,
            "cited_to": self.CITED_TO,
        }
        entry.update(overrides)
        return {key: value for key, value in entry.items() if value is not None}

    def mutated_packet(self, root: Path,
                       origin: str | None = None,
                       old: str = "quoting the ratified prose",
                       new: str = "quoting the corrected prose",
                       **kwargs) -> tuple[Path, str, str]:
        """A ratified packet whose origin was edited AFTER ratification and
        COMMITTED — the #318 shape, reduced.

        Returns (packet directory, ratifying commit, mutating commit), both
        full object names, which is what the record must carry.
        """
        directory = self.packet(
            root, origin=self.ORIGIN if origin is None else origin, **kwargs)
        ratified_at = self.sha(root)
        self.mutate(directory, old, new)
        commit_all(root, "reword the origin after ratification")
        return directory, ratified_at, self.sha(root)

    def refusal(self, root: Path, directory: Path,
                change: str = "change-r") -> str:
        errors = support.origin_retention_errors(root, directory,
                                                 change=change)
        self.assertTrue(errors, "expected a refusal, got none")
        return "\n".join(errors)

    def test_an_accepted_disposition_moves_the_baseline_and_archives(self):
        """THE WHOLE CHANNEL, END TO END. Without the record the archive dies
        on the origin-retention gate; with it, the SAME call gets past that
        gate and dies on the next one — which is the shape #318 measured by
        hand when it restored the bytes in a throwaway worktree."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            (directory / "tasks.md").write_text(
                "## 1. Work\n\n- [ ] 1.1 Archive this change\n",
                encoding="utf-8")

            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)

            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at))
            commit_all(root, "record the owner's acceptance")

            with mock.patch("builtins.print") as printed:
                self.assertEqual(
                    support.origin_retention_errors(root, directory), [])
            said = "\n".join(str(call.args[0])
                             for call in printed.call_args_list)
            # THE ACCEPTANCE IS ANNOUNCED, never silent
            self.assertIn("ORIGIN DISPOSITION ACCEPTED change-r", said)
            self.assertIn(mutation_at[:12], said)
            self.assertIn("Brett Heap", said)
            self.assertIn(self.WORD, said)
            self.assertIn(self.CITED_TO, said)
            self.assertIn("ORIGIN RETAINED change-r", said)

            # …and the archive now reaches the NEXT gate, which is the proof
            # that it got past this one
            with self.assertRaises(support.SupportError) as caught:
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)
            self.assertNotIsInstance(caught.exception,
                                     support.OriginRetentionError)
            self.assertIn("incomplete tasks", str(caught.exception))

    def test_an_unreadable_accepted_declaration_refuses_the_acceptance(self):
        """THE TWO READS THE FAIL-CLOSED PASS LEFT ALONE, pinned rather than
        changed (PR #1024's bench, second round).

        Every read under the origin-retention walk now separates ABSENT from
        UNREADABLE, and `_accept_declaration_problems` was MEASURED instead
        of altered: the acceptance turns on what the dispositioned commit
        DECLARED, and a blob git cannot read is not a declaration. The entry
        fails its own predicate, the headline mutation finding stands, and
        the archive refuses — which is the answer a fail-closed read would
        have reached anyway, arrived at through a check the record already
        carried. So the code stayed as it was and the property is pinned
        here, where a later reader who flattens either read into an
        acceptance has to fail a fixture to do it.

        BOTH HALVES USE A REAL UNREADABLE OBJECT, deleted out of
        `.git/objects` rather than mocked, in the shape the sibling lineage
        fixtures already use. The second half is the ORDERING that makes the
        record's other read safe: the declaration AT RATIFICATION goes
        through `_readable_blob` BEFORE any disposition is consulted, so a
        silence there refuses `origin-retention-history-unreadable` and the
        record — valid, committed, and naming that very commit — is never
        reached at all."""
        rel = "openspec/changes/change-r/.openspec.yaml"

        def make_unreadable(root: Path, revision: str) -> None:
            blob = subprocess.run(
                ["git", "-C", str(root), "rev-parse", f"{revision}:{rel}"],
                check=True, capture_output=True, text=True).stdout.strip()
            loose = root / ".git" / "objects" / blob[:2] / blob[2:]
            if not loose.exists():
                self.skipTest("this fixture's objects were packed, so there "
                              "is no loose blob to make unreadable")
            loose.unlink()
            self.assertIsNone(support.git_show_text(root, revision, rel))

        # THE RECORD'S OWN READ. The acceptance holds while git answers…
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at))
            commit_all(root, "record the owner's acceptance")
            with mock.patch("builtins.print"):
                self.assertEqual(
                    support.origin_retention_errors(root, directory), [])

            # …and stops holding the moment it cannot read what it accepted
            make_unreadable(root, mutation_at)
            joined = "\n".join(support.origin_retention_errors(root,
                                                               directory))
            self.assertIn("the origin declaration differs from the one this "
                          "change was ratified over", joined)
            self.assertIn("there is no declaration to accept", joined)
            with self.assertRaises(support.OriginRetentionError):
                support.archive_change(root, "change-r", "2026-09-05",
                                       False, True)

        # THE BASELINE READ IS ASKED FIRST, which is the whole reason the
        # read above is the only one a record can reach over a silence.
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at))
            commit_all(root, "record the owner's acceptance")
            make_unreadable(root, ratified_at)
            with self.assertRaises(support.OriginRetentionError) as caught:
                support.origin_retention_errors(root, directory)
            self.assertIn("origin-retention-history-unreadable",
                          str(caught.exception))
            self.assertIn(f"the blob `{rel}` stands as at "
                          f"{ratified_at[:12]}", str(caught.exception))

    def test_the_318_tense_only_approved_by_case_archives_with_the_record(self):
        """THE LIVE CASE, with #318's own bytes. The mutation is the TENSE of
        one sentence inside the `approved_by` folded scalar — who approved,
        when, the verbatim word and what the word authorized are all
        unchanged — and it landed fourteen minutes after the ratification in
        the same pull request. `changed keys: approved_by`, and nothing else
        moved."""
        was = (
            "origin:\n"
            "  kind: ad_hoc\n"
            "  id: codexfactory:adhoc:2026-09-06-floor-regeneration-automation\n"
            "  reason: the floor regeneration lane is proposed as an ad-hoc\n"
            "  approved_by: >-\n"
            "    Brett Heap, 2026-09-06 — AUTHORITY TO AUTHOR, NOT A\n"
            "    RATIFICATION OF CONTENT. The packet remains Status: draft, it\n"
            "    carries no ratification citation, and none is owed.\n"
            "  approved_on: '2026-09-06'\n"
        )
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(
                root, origin=was,
                old="The packet remains Status: draft, it",
                new="At the time this field was written the packet WAS\n"
                    "    Status: draft, it")

            refused = self.refusal(root, directory)
            self.assertIn("changed keys: approved_by", refused)

            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at,
                fact="the TENSE of one sentence was rewritten so it reads "
                     "coherently beside the ratification paragraph appended "
                     "in the same pull request; kind/id/reason/approved_on "
                     "and the substance of approved_by are unchanged"))
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_with_no_record_the_refusal_names_the_channel_and_its_fields(self):
        """THE REFUSAL MUST ROUTE THE READER. #318 held a recorded acceptance
        and the gate's last word was "this gate has no bypass flag", which is
        true and told that operator nothing they could act on."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, _mutation = self.mutated_packet(root)
            refused = self.refusal(root, directory)
            self.assertIn("contested-class act", refused)
            self.assertIn("no bypass flag", refused)
            # the PATH, in the root the gate was given
            self.assertIn(str(support.origin_dispositions_path(root)),
                          refused)
            self.assertIn("schema_version: 1", refused)
            self.assertIn("kind: origin_dispositions", refused)
            # every field an entry must carry
            for field in support.ORIGIN_DISPOSITION_KEYS:
                self.assertIn(field, refused)
            # …and this change's own ratifying commit, IN FULL, so the entry
            # can be written straight out of the refusal
            self.assertIn(ratified_at, refused)
            # BOTH repairs are named, not only the record
            self.assertIn("RESTORE", refused)

    def test_the_record_is_read_from_the_root_the_gate_was_given(self):
        """THE CONSUMER PROPERTY. This script runs as
        `$OPENXFACTORY_ROOT/scripts/proposal-support.py <consumer-root>
        archive <id>`, so the record must be the CONSUMER's — read from the
        root argument and not from wherever the script itself lives."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            entry = self.accept_entry("change-r", ratified_at, mutation_at)
            self.assertEqual(
                support.origin_dispositions_path(root),
                root.resolve() / "openspec" / "origin-dispositions.yaml")
            # the right record in the WRONG place changes nothing
            self.write_record(root, entry, rel="origin-dispositions.yaml")
            self.assertTrue(support.origin_retention_errors(root, directory))
            # …and in the right place it is read
            self.write_record(root, entry)
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_a_record_for_another_change_id_is_ignored(self):
        """An entry disposing SOME OTHER change is not this change's record,
        and is not validated either — one change's bad entry must never block
        another change's archive."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-z", ratified_at, mutation_at, word=None))
            refused = self.refusal(root, directory)
            self.assertIn("no bypass flag", refused)
            # the OTHER change's entry is not reported as a defect of this one
            self.assertNotIn("origin disposition:", refused)
            self.assertNotIn("change-z", refused)

    def test_an_accepted_mutation_does_not_license_the_next_one(self):
        """ANTI-VACUITY, AND THE REASON THIS IS NOT A BYPASS. An acceptance
        MOVES the baseline to the accepted declaration; it does not switch the
        comparison off. A second, undispositioned edit on top of an accepted
        one refuses exactly as the first one did.

        AND THE REFUSAL SUBTRACTS FOR THE OPERATOR (Copilot, round 2 on PR
        #891). The headline finding compares the tree to the RATIFICATION and
        so names the UNION — the accepted key and the new one — because the
        baseline does not move on a record whose predicate failed. The
        record's own finding names the difference that is actually
        undispositioned, and diffs against the accepted declaration rather
        than against the ratified one."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at))
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])
            self.mutate(directory, "  approved_on: '2026-09-05'",
                        "  approved_on: '2026-09-08'")
            refused = self.refusal(root, directory)
            self.assertIn("SECOND, undispositioned mutation", refused)
            self.assertIn(mutation_at[:12], refused)
            self.assertIn("-  approved_on: '2026-09-05'", refused)
            self.assertIn("+  approved_on: '2026-09-08'", refused)
            # the SUBTRACTION: only the undispositioned key, and the headline
            # above it still names the union it measured against ratification
            self.assertIn(
                "keys moved BEYOND the accepted declaration: approved_on",
                refused)
            self.assertIn("changed keys: approved_by, approved_on", refused)

    def test_a_record_naming_a_mutation_that_is_not_a_commit_refuses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, _mutation = self.mutated_packet(root)
            absent = "0" * 40
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, absent))
            refused = self.refusal(root, directory)
            self.assertIn("not a commit in this repository", refused)
            self.assertIn(absent[:12], refused)

    def test_a_record_whose_mutation_precedes_the_ratification_refuses(self):
        """A POST-ratification mutation is one that comes AFTER it. An entry
        naming an earlier commit is disposing something else."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, _mutation = self.mutated_packet(root)
            creation = self.sha(root, f"{ratified_at}^")
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, creation))
            refused = self.refusal(root, directory)
            self.assertIn("does not DESCEND from the ratifying commit",
                          refused)

    def test_a_record_whose_ratified_at_is_not_the_ratifying_commit_refuses(self):
        """The gate resolves the ratifying commit from HISTORY and does not
        take the entry's word for it: an entry naming some other baseline
        disposes a mutation of that baseline, not of this one."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            wrong = self.sha(root, f"{ratified_at}^")
            self.write_record(root, self.accept_entry(
                "change-r", wrong, mutation_at))
            refused = self.refusal(root, directory)
            self.assertIn("some other baseline", refused)
            self.assertIn(ratified_at[:12], refused)
            self.assertIn(wrong[:12], refused)

    def test_a_record_declaring_an_extra_changed_key_refuses(self):
        """AN ACCEPTANCE COVERS EXACTLY THE KEYS IT NAMES. A wider key set is
        an acceptance of mutations that did not happen, and the operator who
        writes one has not read the diff they are accepting."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at,
                changed_keys=("approved_by", "reason")))
            refused = self.refusal(root, directory)
            self.assertIn("changed_keys", refused)
            self.assertIn("['approved_by', 'reason']", refused)
            self.assertIn("['approved_by']", refused)

    def test_a_record_declaring_too_few_changed_keys_refuses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at, changed_keys=()))
            refused = self.refusal(root, directory)
            self.assertIn("touches ['approved_by']", refused)

    def test_a_disposition_other_than_accept_refuses(self):
        """ONLY `accept` NEEDS A RECORD. A restoration is the BYTES: put the
        ratified declaration back and this gate passes with nothing to read,
        so a `restore` entry is a record of an act the tree has not
        performed."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            for value in ("restore", "accepted", "ACCEPT", "noted"):
                with self.subTest(disposition=value):
                    self.write_record(root, self.accept_entry(
                        "change-r", ratified_at, mutation_at,
                        disposition=value))
                    refused = self.refusal(root, directory)
                    self.assertIn(f"`disposition` is {value!r}", refused)
                    self.assertIn("RESTORING the ratified declaration needs "
                                  "no record", refused)

    def test_a_record_missing_a_required_field_refuses_naming_it(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            for field in support.ORIGIN_DISPOSITION_KEYS:
                if field == "change_id":
                    continue  # an entry without one names no change at all
                with self.subTest(missing=field):
                    entry = self.accept_entry(
                        "change-r", ratified_at, mutation_at)
                    entry.pop(field)
                    self.write_record(root, entry)
                    refused = self.refusal(root, directory)
                    self.assertIn(f"is missing {field}", refused)

    def test_an_unknown_key_refuses_and_the_two_near_misses_are_named(self):
        """A KEY THIS GATE DOES NOT READ CANNOT NARROW WHAT THE ENTRY ACCEPTS,
        so a typo is refused rather than ignored. The two near-misses are
        named because they are real spellings ELSEWHERE in this estate — an
        author reaching for one has picked a sibling record's word rather than
        mistyped: `recorded_at` (every `_at` key here names a commit, and the
        citation is `cited_to`) and `why` (`openspec-cli-pin.yaml`'s narrative
        key, where this record follows `archive-date-dispositions.yaml`'s
        `fact`)."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at,
                recorded_at=self.CITED_TO, why="a tense-only rewording"))
            refused = self.refusal(root, directory)
            self.assertIn("unknown key(s) recorded_at, why", refused)
            self.assertIn("spells the citation `cited_to`", refused)
            self.assertIn("spells the narrative `fact`", refused)

    def test_a_citation_may_be_a_list_and_an_uncited_entry_refuses(self):
        """A DISPOSITION WITHOUT A CITATION IS REFUSED, NOT IGNORED — the rule
        `openspec-cli-pin.yaml` states in those words. WHAT it points at is
        not pattern-matched: the sibling records cite issues, pull requests,
        spec lines and council rulings, so a list of prose citations is as
        lawful here as one URL, and only EMPTINESS refuses."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            entry = self.accept_entry("change-r", ratified_at, mutation_at)

            # the pin manifest's own shape: a LIST, and prose in it
            entry["cited_to"] = [
                self.CITED_TO,
                "codeXfactory/codexFactory#318 — the ledger and both refusals",
                "opensoft/openxFactory#745 — the channel this entry uses"]
            self.write_record(root, entry)
            with mock.patch("builtins.print") as printed:
                self.assertEqual(
                    support.origin_retention_errors(root, directory), [])
            said = "\n".join(str(call.args[0])
                             for call in printed.call_args_list)
            # …and the ANNOUNCEMENT reads it out as prose, not as a Python
            # list repr (Copilot, round 1): brackets and quotes in operator
            # output are noise, and the three citations are one sentence
            self.assertIn("; ".join(entry["cited_to"]), said)
            self.assertNotIn("['" + self.CITED_TO, said)

            for empty in ([], "", "   ", [self.CITED_TO, ""]):
                with self.subTest(cited_to=empty):
                    entry["cited_to"] = empty
                    self.write_record(root, entry)
                    refused = self.refusal(root, directory)
                    self.assertIn("`cited_to` must be a non-empty string",
                                  refused)

    def test_an_abbreviated_object_name_refuses(self):
        """A citation is a FULL object name; an abbreviation is ambiguous by
        construction — the rule `archive-date-dispositions.yaml` states."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at[:12]))
            refused = self.refusal(root, directory)
            self.assertIn("FULL 40-hex object name", refused)

    def test_an_unquoted_date_is_refused_with_the_yaml_trap_named(self):
        """YAML reads a bare `2026-09-10` as a DATE, which is why the sibling
        record's header says every entry scalar is quoted."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            text = self.record_text(self.accept_entry(
                "change-r", ratified_at, mutation_at)).replace(
                    '"2026-09-10"', "2026-09-10")
            self.write_record(root, text=text)
            refused = self.refusal(root, directory)
            self.assertIn("`disposed_on` must be a non-empty string", refused)
            self.assertIn("quote it", refused)

    def test_two_entries_for_one_change_refuse_as_ambiguous(self):
        """ONE entry names the accepted declaration. A later accepted mutation
        REPLACES it — moving `mutation_at` forward and widening `changed_keys`
        to the whole diff from the ratifying commit — rather than sitting
        beside it, because two entries make "the origin of record" a
        question."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            self.write_record(
                root,
                self.accept_entry("change-r", ratified_at, mutation_at),
                self.accept_entry("change-r", ratified_at, ratified_at))
            refused = self.refusal(root, directory)
            self.assertIn("2 entries name change-r", refused)
            self.assertIn(mutation_at, refused)

    def test_an_entry_that_disposes_nothing_refuses(self):
        """A STALE OR VACUOUS ENTRY IS A DEFECT, the rule the sibling record
        already states. An entry whose `mutation_at` carries the RATIFIED
        declaration accepts nothing, and reading it as an acceptance of
        whatever the tree happens to hold is exactly the bypass this design
        refuses to become."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory = self.packet(root)
            ratified_at = self.sha(root)
            (directory / "tasks.md").write_text(
                "## 1. Work\n\n- [x] 1.1 Done\n- [x] 1.2 Also done\n",
                encoding="utf-8")
            commit_all(root, "touch the packet without touching its origin")
            innocent = self.sha(root)
            self.mutate(directory, "quoting the ratified prose",
                        "quoting the corrected prose")
            commit_all(root, "mutate the origin after ratification")
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, innocent))
            refused = self.refusal(root, directory)
            self.assertIn("IDENTICAL to the ratified one", refused)
            self.assertIn("disposes nothing", refused)

    def test_a_malformed_record_refuses_naming_the_file(self):
        """A file at this path that is not this record cannot be read as an
        empty one: "no dispositions" and "the wrong file" are different
        answers, and only one of them is the operator's to fix."""
        with TemporaryDirectory() as td:
            root = Path(td)
            directory, ratified_at, mutation_at = self.mutated_packet(root)
            entry = self.accept_entry("change-r", ratified_at, mutation_at)
            cases = {
                "cannot be read": "dispositions: [ unclosed\n",
                "`schema_version` is 2": self.record_text(
                    entry, schema_version=2),
                "`kind` is 'archive_date_dispositions'": self.record_text(
                    entry, kind="archive_date_dispositions"),
                "`dispositions` must be a list":
                    "schema_version: 1\nkind: origin_dispositions\n"
                    "dispositions: {}\n",
                "must be a mapping": "- just a list\n",
            }
            for expected, text in cases.items():
                with self.subTest(record=expected):
                    self.write_record(root, text=text)
                    refused = self.refusal(root, directory)
                    self.assertIn("openspec/origin-dispositions.yaml",
                                  refused)
                    self.assertIn(expected, refused)

    def test_the_support_manifest_is_measured_against_the_accepted_origin(self):
        """THE SECOND COPY MOVES WITH THE BASELINE. The manifest arm compares
        the support manifest's repeated origin fields against the declaration
        of record; once a mutation is accepted, that declaration is the
        ACCEPTED one — comparing to the superseded ratified declaration would
        refuse a manifest that is correct, and not comparing at all would drop
        an arm the requirement names."""
        accepted_id = "fixture:staging:topic-s"
        with TemporaryDirectory() as td:
            root = Path(td)
            manifest = {"format_version": 1, "files": [],
                        "origin": {"kind": "staged",
                                   "id": "fixture:staging:topic-r",
                                   "path": "ideation/staging/topic-r"}}
            directory, ratified_at, mutation_at = self.mutated_packet(
                root, origin=self.STAGED_ORIGIN, manifest=manifest,
                old="fixture:staging:topic-r", new=accepted_id)
            self.write_record(root, self.accept_entry(
                "change-r", ratified_at, mutation_at, changed_keys=("id",)))

            # the manifest still repeats the SUPERSEDED id: refused, and the
            # finding names the accepted declaration as what it must match
            refused = self.refusal(root, directory)
            self.assertIn("support manifest origin `id`", refused)
            self.assertIn(f"the ACCEPTED declaration at {mutation_at[:12]}",
                          refused)
            self.assertIn(repr(accepted_id), refused)

            manifest_path = directory / "supporting-docs" / "manifest.yaml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    "fixture:staging:topic-r", accepted_id),
                encoding="utf-8")
            self.assertEqual(
                support.origin_retention_errors(root, directory), [])

    def test_the_archive_help_names_the_disposition_channel(self):
        """THE HELP SURFACE ROUTES THE READER TOO. An operator holding the
        owner's acceptance found nothing on this surface and nothing in the
        refusal but "no bypass flag" (codeXfactory/codexFactory #318), so the
        subcommand's own help now names BOTH repairs and the record. It names
        no flag — the sibling test below reads this same text."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), ".", "archive", "--help"],
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ORIGIN RETENTION", result.stdout)
        self.assertIn("RESTORE", result.stdout)
        self.assertIn("ACCEPT", result.stdout)
        self.assertIn(support.ORIGIN_DISPOSITIONS_REL, result.stdout)
        self.assertIn("There\nis no flag for it.", result.stdout)

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
