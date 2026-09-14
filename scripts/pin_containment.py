"""The containment dialect two callers share: a claimed path resolved inside a
root, and a root's `contracts/` registry boundary checked BEFORE it is used.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
It is the third neutral module, created for the reason the first two were
(`output_boundary.py`, `path_slug.py`): a helper two callers need cannot live
inside one of them without making the other reach across a seam. Its two
callers are `scripts/validate-pin-registrations.py` — a standalone checker that
declines to import doc-health package members — and
`scripts/doc_health/families.py`'s pinned-target arm. Ratified by
`extend-prose-tagging-target-to-pinned-capabilities` (design D-2, task 3.3(m)),
which requires the arm to reuse this repository's containment dialect "rather
than inventing a second one" and requires the helper to RECEIVE THE RESOLVING
REPOSITORY ROOT AS A PARAMETER, because `resolve_in_tree`'s module-global
`ROOT` cannot speak for the per-repository and fixture roots doc-health runs
against.

WHAT THE DIALECT IS, AND THE TWO QUESTIONS IT ANSWERS. The first question is
the one `resolve_in_tree` already answered and still answers: does a CLAIMED
relative path stay inside a given root once resolved? The second is new and is
the one the REPOSITORY question cannot answer — does it stay inside a named
BOUNDARY DIRECTORY of that root? A committed
`contracts/foo-pin.yaml -> ../openspec/specs/...` symlink stays inside the
repository and passes the first; only the second refuses it.

AND THE BOUNDARY ITSELF IS CHECKED BEFORE ANY CANDIDATE IS. A boundary that can
be redirected is not a boundary: where `<root>/contracts` is ITSELF a symlink to
another directory, a caller comparing a candidate against
`(root / "contracts").resolve()` accepts and READS a file outside the lexical
registry the boundary names — the redirection having moved the boundary rather
than been caught by it, and the comparison still passing. `boundary_dir` is
therefore a PRECONDITION on the root, answered before a candidate exists.

THE REFUSAL REASONS ARE OPERATOR OUTPUT, NOT FINDING TEXT. A reason may quote a
RESOLVED host-absolute path, which is exactly what a human debugging a refusal
needs and exactly what the constitution's Article IV forbids a COMMITTED file to
carry. A caller whose output is committed — a doc-health finding rendered into
`health/` — must therefore write its own sentence from the refusal CODE and name
its root by repository name, never by interpolating the reason.

Nothing here reads a file. `is_dir`, `is_symlink` and `resolve` interrogate the
filesystem's metadata; no caller of this module opens anything through it.
"""

from __future__ import annotations

from pathlib import Path

#: The registry directory a pin record must be a file of. One spelling, so a
#: caller cannot quietly police a different directory than the one this
#: module's precondition checked.
CONTRACTS_DIRNAME = "contracts"

#: Refusal codes, so a caller can branch on the DEFECT without matching prose.
NOT_A_PATH = "not-a-path"
ABSOLUTE = "absolute"
TRAVERSAL = "traversal"
OUTSIDE_ROOT = "outside-root"
OUTSIDE_BOUNDARY = "outside-boundary"
BOUNDARY_MISSING = "boundary-missing"
BOUNDARY_NOT_A_DIRECTORY = "boundary-not-a-directory"
BOUNDARY_REDIRECTS = "boundary-redirects"
UNRESOLVABLE = "unresolvable"


def resolve_in_root(claimed, root, *, boundary=None):
    """The claimed path resolved inside `root`, or a REFUSAL.

    Returns `(path, None)` or `(None, (code, reason))`. `root` is the tree the
    claim is made about — a parameter rather than a module global, because the
    two callers speak for different trees and doc-health speaks for several
    within one run.

    Exists because `Path(root) / "/abs"` DISCARDS the root: a claim naming an
    absolute or `..`-escaping path would otherwise be reported "in this tree"
    whenever the HOST happens to carry that file, while no consumer's checkout
    contains it. The constitution's Article IV says the same thing about the
    corpus — "Committed files MUST NOT contain host-absolute paths; use
    repo-relative paths or runtime resolution" — so a register naming one is a
    finding on its own terms and not merely an unreadable path.

    `boundary`, when given, is a directory the RESOLVED path must also stay
    inside — the `contracts/` question rather than the repository one. Pass the
    directory `boundary_dir` returned, never a freshly-joined
    `root / "contracts"`: the precondition is what makes the comparison
    meaningful.
    """
    if not isinstance(claimed, str) or not claimed.strip():
        return None, (NOT_A_PATH,
                      "is not a non-empty string path, and `ROOT / "
                      "<non-string>` raises rather than reporting")
    candidate = Path(claimed)
    if candidate.is_absolute():
        return None, (ABSOLUTE,
                      "is an ABSOLUTE path; joining one to the repository root "
                      "discards the root entirely, and no consumer's checkout "
                      "carries a host path")
    if ".." in candidate.parts:
        return None, (TRAVERSAL,
                      "contains a '..' segment, which walks out of the "
                      "repository the register speaks for")
    try:
        resolved_root = Path(root).resolve()
        target = (resolved_root / candidate).resolve()
    except (OSError, RuntimeError, ValueError):
        return None, (UNRESOLVABLE,
                      "cannot be resolved — a symlink loop, an unreadable link "
                      "or a malformed path; refused rather than read")
    if not target.is_relative_to(resolved_root):
        return None, (OUTSIDE_ROOT,
                      f"resolves to {target}, which is outside the repository; "
                      f"refused rather than read")
    if boundary is not None and not target.is_relative_to(Path(boundary)):
        return None, (OUTSIDE_BOUNDARY,
                      f"resolves to {target}, which is outside the "
                      f"{Path(boundary).name}/ directory it must stay inside; "
                      f"refused rather than read")
    return target, None


def boundary_dir(root, name=CONTRACTS_DIRNAME):
    """`<root>/<name>` as a REAL, NON-REDIRECTING directory, or a REFUSAL.

    Returns `(path, None)` or `(None, (code, reason))`. The three conditions are
    the boundary precondition in full: it EXISTS AS A DIRECTORY, it is NOT A
    SYMLINK, and its RESOLVED path equals its LEXICAL path. The third catches
    the case the first two do not — a directory reached through a symlinked
    ANCESTOR — and together they are what make `resolve_in_root`'s `boundary`
    comparison a statement about the lexical registry rather than about wherever
    a redirection led.

    Nothing is read here and no candidate is built. A caller that gets a
    refusal refuses FOR THAT ROOT as a whole: every candidate that would be
    resolved through it is affected, and the defect is the registry directory
    rather than any one record.

    THE ROOT IS RESOLVED FIRST AND THE NAME JOINED TO THAT, so the third
    condition speaks about `<name>` and not about the root's own ancestry: a
    checkout that itself sits under a symlinked directory — `/tmp` on some
    hosts, a developer's symlinked workspace — would otherwise fail the
    lexical-equality test for every root, refusing a registry nothing is wrong
    with.
    """
    try:
        lexical = Path(root).resolve() / name
    except (OSError, RuntimeError, ValueError):
        return None, (UNRESOLVABLE,
                      "cannot be resolved — a symlink loop, an unreadable link "
                      "or a malformed path; refused rather than read")
    # THE SYMLINK TEST COMES FIRST: `exists()` FOLLOWS a link, so a DANGLING
    # `contracts` symlink would otherwise read as "missing" and send the operator
    # to `mkdir` a directory a link already occupies (PR #1040 round 6).
    if lexical.is_symlink():
        return None, (BOUNDARY_REDIRECTS,
                      f"has a {name} that is a SYMLINK; a boundary that can be "
                      f"redirected is not a boundary, so no candidate is "
                      f"resolved through it")
    if not lexical.exists():
        return None, (BOUNDARY_MISSING,
                      f"carries no {name}/ directory to resolve a record in")
    if not lexical.is_dir():
        return None, (BOUNDARY_NOT_A_DIRECTORY,
                      f"has a {name} that is not a directory")
    try:
        redirected = lexical.resolve() != lexical
    except (OSError, RuntimeError, ValueError):
        return None, (UNRESOLVABLE,
                      "cannot be resolved — a symlink loop, an unreadable link "
                      "or a malformed path; refused rather than read")
    if redirected:
        return None, (BOUNDARY_REDIRECTS,
                      f"has a {name} whose resolved path is not its lexical "
                      f"path; a boundary reached through a redirection is not "
                      f"the boundary it names")
    return lexical, None
