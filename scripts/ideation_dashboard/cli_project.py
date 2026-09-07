"""The PROJECT VERBS of the command line: `generate`, `create`, `edit`
(`split-opendox-two-layer-product` § 2.4, PR 4 of 4).

FIXED CORE, NOT AN EXTENSION. Design § D2 files the project cluster in the
openDox column — the layer that keeps the document surface — so these verbs are
registered by `build_parser` directly, exactly as they were. The split here is
by COLUMN, so the § 3 carve is a file move rather than a diff; it is not a
change to how anything is dispatched, and this module deliberately owns no
parser wiring of its own.

WHY `cmd_generate_and_open` IS NOT HERE, recorded because its absence is a
decision and not an omission. That verb is the CLI's ASSEMBLY POINT: its body is
one `serve_mod.build_server(...)` call that declares the notebook adapter, the
model-provider factory and the retrieval backend this install talks to, and § 2.4
PR 3 will declare `route_extensions` at the same call. The repository already
treats it that way — three landed tests read the ENTRYPOINT'S OWN SOURCE to
check those declarations (`test_session_notebook.py`,
`test_doxbench_knowledge_service.py` ×2) — and `serve.py`'s own entrypoint stays
in `serve.py` for the same reason (memo § 4). Composition belongs to the core.

HOW THIS MODULE REACHES THE SHARED SPINE: through `_core()`, resolved at CALL
time and relative to this module's own package, never a module-level
`from ideation_dashboard.cli import _report`. A frozen reference
would still work and would silently stop honouring the module-level patch sites
the existing tests rely on (`cli_mod._generate_and_write`,
`cli_mod._locate_validator` behind `_validate`) — green, and wrong. The
accessor also keeps the two modules importable in either order.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from ideation_dashboard import authoring as authoring_mod
from ideation_dashboard.boundary import HUMAN, OutputBoundary


def _core():
    """The core CLI module OF THIS MODULE'S OWN PACKAGE, resolved when a verb RUNS.

    Deliberately a function and not a module-level import: see the header. Every
    reference this module makes into the shared spine goes through it.

    Deliberately RELATIVE, too: the tree is importable both as
    `ideation_dashboard.x` and as `scripts.ideation_dashboard.x`, each spelling
    its own module object with its own `RepoRootRefused`/`GeneratedAtRefused`, so
    a column that named the core absolutely would raise refusals the running
    `main` cannot catch. `from . import cli` reaches the core that imported this
    column, whichever spelling that was — see `cli_gate._core()` for the long
    form of the argument."""
    from . import cli

    return cli


def cmd_generate(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve()
    snapshot, written = _core()._generate_and_write(args, output)
    _core()._report(snapshot, written, Path(args.repo_root).resolve())
    return _core()._validate(written, args,
                             continues="the snapshot file stands and this command "
                                       "exits 0")


def cmd_create(args: argparse.Namespace, *, launcher=subprocess.Popen) -> int:
    """The human create action (US8/T030): scaffold a header-compliant doc into
    `--area` and, unless `--no-open`, launch the human's editor over it. The
    write is `authoring.create_scaffold`'s one `boundary.create_document` call
    (create-only — an existing target refuses); this command performs no
    further mutation itself.

    `--area` goes through the SAME confinement the gated create uses
    (`authoring.area_refusal` — inside `ideation/`, never inside the gate-records
    prefix). This verb records nothing and opens no session, but it writes into the
    SERVED checkout directly, so a document it drops into the records prefix would
    sit in exactly the blind spot SC-002's fingerprint excludes (PR #49 wave-2
    critic). One definition, every create path."""
    repo_root = Path(args.repo_root).resolve()
    refusal = authoring_mod.area_refusal(args.area)
    if refusal is not None:
        print(f"create refused: {refusal}", file=sys.stderr)
        return 1
    boundary = OutputBoundary(repo_root, actor=HUMAN)
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    written = authoring_mod.create_scaffold(
        boundary, area=args.area, title=args.title, summary=args.summary,
        topics=topics, repository_context=args.repository_context,
        kind=args.kind, possible_feats=args.possible_feat,
    )
    rel = written.relative_to(repo_root).as_posix()
    print(f"wrote {rel}")
    print(written)
    if args.no_open:
        return 0
    argv = authoring_mod.edit_command(repo_root, rel, editor=args.editor)
    try:
        launcher(argv)
    except Exception as exc:  # no editor/opener available — never fatal
        print(f"  (could not launch an editor: {exc}; open {written} manually)")
    return 0


def cmd_edit(args: argparse.Namespace, *, launcher=subprocess.Popen) -> int:
    """Select-to-edit (US8/T030): launch the human's editor over any listed
    document. Read-only from the dashboard's side — `edit_target` only
    resolves the path; the dashboard itself modifies nothing."""
    repo_root = Path(args.repo_root).resolve()
    path = authoring_mod.edit_target(repo_root, args.path)
    print(path)
    if args.no_open:
        return 0
    argv = authoring_mod.edit_command(repo_root, args.path, editor=args.editor)
    try:
        launcher(argv)
    except Exception as exc:  # no editor/opener available — never fatal
        print(f"  (could not launch an editor: {exc}; open {path} manually)")
    return 0
