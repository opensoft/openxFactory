#!/usr/bin/env python3
"""Install the PINNED OpenSpec CLI and put it on PATH. Judge nothing.

WHAT THIS IS, AND WHAT IT IS NOT. This is an INSTALLER. A green exit means
exactly one thing: the bytes `contracts/openspec-cli-pin.yaml` names were
fetched, their SHA-512 and SHA-1 were recomputed and matched, the artifact was
installed, and the resulting executable reports the pinned version. It is NOT a
validation verdict. It opens no governed surface, reads no delta, and says
nothing whatever about whether this repository's corpus is valid. A required
check that wants a VERDICT must call
`scripts/validate-openspec-cli-pin.py --all` and read its exit code; this file
cannot answer that question and does not pretend to.

WHY IT EXISTS. `tests/proposal-support/` drives the REAL `openspec` binary
through the archive wrapper — three of its tests carry
`@unittest.skipUnless(shutil.which("openspec"), …)` and are the only reason the
`pytest-suite` job installs the CLI at all. That job used to install it by
literal (`npm install -g @fission-ai/openspec@1.2.0`), which was a SECOND copy
of a pin the repository already held, and the two duly moved apart: the pin went
to `1.12.0` while the workflow still installed `1.2.0`, so the required test
suite drove one version while the `openspec-cli-pin` gate verified another. This
script closes that by making the test job resolve its binary THROUGH the pin, so
the suite drives the same bytes the gate verified and the version is written in
exactly one place.

WHY IT IS NOT A FLAG ON THE VERIFIER. The obvious shape — `--verify-only` on
`scripts/validate-openspec-cli-pin.py` — is FORBIDDEN by that file's own
docstring, and the prohibition is a ratified contract decision rather than a
style preference: `neutral-product-pin` requires that a pinned validator invoked
with no scan target REFUSE rather than self-test, "because a self-test that opens
no governed surface is a green check that verified nothing", and
`test_there_is_no_verify_only_mode` asserts the absence. Adding the flag would
put that hole back behind a convenience. This task does not reopen that decision,
so the install lives HERE, under its own name, where nothing can mistake its exit
code for a verdict about the corpus. Nothing is re-implemented: the pin is read,
parsed, fetched, hashed and installed by the verifier's OWN functions, imported
from the verifier's own file. The version and the integrity are written nowhere
in this file.

WHAT IT DOES WITH ITS RESULT. It prints the executable's path on stdout, and —
when `$GITHUB_PATH` names a file, as it does on a GitHub runner — APPENDS the
executable's directory to that file, which is how a step hands a PATH entry to
the steps after it. The append is an ordinary file write rather than a redirected
`echo`, so a failure to perform it is an error this script reports rather than a
line that silently went nowhere.

THE INSTALL OUTLIVES THE PROCESS, deliberately. The verifier's own default is a
`TemporaryDirectory` discarded when the run ends, which is right for a gate that
validates in the same process and wrong here: a binary that vanishes when this
script exits is a binary no later step can run. So the install goes to a named
directory that persists — `--cache-dir`, defaulting to the verifier's own
`default_cache_root()` so a developer's installs are shared with it rather than
duplicated beside it — and only the FETCH workspace is emptied, at the START of
each run rather than the end. That order matters: `fetch_artifact` requires
exactly one tarball in its destination and refuses an ambiguous fetch, so a
tarball left behind by a PREVIOUS pin version would turn the next run after a
bump into `pin-unresolvable`. Emptying first makes the workspace as clean as a
temporary directory while keeping the path stable.

THE TARBALL IS RE-VERIFIED ON EVERY RUN regardless of the cache — that is
`resolve_pinned`'s property, not this file's, and it is the reason a persistent
install directory is not a trust shortcut: only the INSTALL is reused, and only
from a directory named and stamped with the verified content address.

Exit codes:
  0  the pinned artifact verified, installed, and reported the pinned version
  2  ANY refusal — the verifier's own `PinRefusal`, printed verbatim with its
     remediation trailer — and any environment failure of this script's own

  There is no exit 1. Exit 1 belongs to the verifier and means "the pin held and
  your deltas are invalid", which is a sentence about a corpus this script never
  opens. Inventing an exit 1 here would give a caller that branches on 0/1/2 a
  third meaning for a code that already has two.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "validate-openspec-cli-pin.py"


def _load_verifier():
    """The pin verifier, LOADED rather than re-implemented.

    The file's name is hyphenated, so it is not importable by name; this is the
    same `spec_from_file_location` route `tests/openspec_cli_pin/` already takes
    to reach it. Loading it — rather than copying its parser, its hashing or its
    install logic — is the whole point: a second implementation of "which bytes
    does the pin name" would be the second copy of the pin this script exists to
    remove.
    """
    spec = importlib.util.spec_from_file_location(
        "openspec_cli_pin_verifier", VERIFIER)
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable
        raise SystemExit(
            f"install-pinned-openspec-cli: {VERIFIER} could not be loaded as a "
            "module; the pinned CLI cannot be resolved without it")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verifier = _load_verifier()


def build_parser() -> argparse.ArgumentParser:
    """Three options, and no scan target of any kind.

    `--all`, `--change`, `--strict`, `--repo`, `--path-mode`, `--tarball` and
    `--verify-only` are all ABSENT and their absence is asserted by a test. This
    tool takes no validation target because it performs no validation; an option
    that looked like one would invite a caller to read this exit code as the
    verdict `scripts/validate-openspec-cli-pin.py` is the only thing that gives.
    """
    parser = argparse.ArgumentParser(
        prog="install-pinned-openspec-cli.py",
        description=(
            "Install the OpenSpec CLI pinned by contracts/openspec-cli-pin.yaml "
            "— verifying the artifact's content address first — and append its "
            "directory to $GITHUB_PATH. This INSTALLS; it does not validate, "
            "and a green exit is not a verdict about any corpus."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--cache-dir", metavar="PATH", default=None,
        help=("the directory verified installs are kept in and reused from "
              "(default: the verifier's own cache root, so the two share one "
              "install). On a runner, pass a path under $RUNNER_TEMP"))
    parser.add_argument(
        "--npm", metavar="BIN", default="npm",
        help="the npm executable to fetch and install with (tests)")
    parser.add_argument(
        "--pin", metavar="PATH", default=None,
        help="an alternative pin file (tests)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        pin = verifier.read_pin(
            Path(args.pin) if args.pin else verifier.PIN_PATH)
        version = verifier.pinned_version(pin)
        integrity, shasum = verifier.pinned_integrity(pin)
        package = verifier.pinned_package(pin)
        binary = verifier.pinned_binary(pin)

        cache_root = (Path(args.cache_dir).expanduser() if args.cache_dir
                      else verifier.default_cache_root())
        # Emptied at the START of the run and left in place at the end — see the
        # module docstring. `.fetch` sits beside the install prefixes rather than
        # above them so that ONE `--cache-dir` names everything this run writes.
        workspace = cache_root / ".fetch"
        shutil.rmtree(workspace, ignore_errors=True)
        workspace.mkdir(parents=True, exist_ok=True)

        executable = verifier.resolve_pinned(
            package, version, integrity, shasum, binary, workspace, cache_root,
            npm=args.npm)
        reported = verifier.assert_reported_version(executable, version)
    except verifier.PinRefusal as exc:
        # Printed VERBATIM, trailer and all. This script adds no wording of its
        # own to a refusal: the verifier owns the refusal vocabulary and the one
        # fixed remediation, and a caller branching on the code must see the code
        # the verifier raised.
        print(str(exc), file=sys.stderr)
        return 2

    print(f"install-pinned-openspec-cli: {package}@{reported} verified against "
          f"its content address (integrity {integrity[:23]}…) and installed at "
          f"{executable}. THIS IS AN INSTALL AND NOT A VERDICT: no delta was "
          f"read and no corpus was validated.", file=sys.stderr)

    github_path = os.environ.get("GITHUB_PATH")
    if github_path:
        try:
            with open(github_path, "a", encoding="utf-8") as handle:
                handle.write(f"{executable.parent}\n")
        except OSError as exc:
            # NOT a `PinRefusal`. The refusal vocabulary is fixed and describes
            # disagreements between a pin and an environment; "this runner's
            # $GITHUB_PATH file could not be written" is neither, and inventing a
            # code for it would put a name into a vocabulary other code branches
            # on. It still exits 2, because a pinned binary nothing can reach is
            # not an installed one.
            print(f"install-pinned-openspec-cli: the pinned CLI installed at "
                  f"{executable}, but $GITHUB_PATH ({github_path}) could not be "
                  f"appended to: {exc}. Later steps would not find `{binary}` on "
                  f"PATH and the tests that need it would SKIP rather than fail, "
                  f"so this is reported here instead of discovered as a moved "
                  f"skip count.", file=sys.stderr)
            return 2
        print(f"install-pinned-openspec-cli: {executable.parent} appended to "
              f"$GITHUB_PATH", file=sys.stderr)

    print(executable)
    return 0


if __name__ == "__main__":
    sys.exit(main())
