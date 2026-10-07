"""Strict filesystem probes: only ABSENCE reads as absent (#1201).

WHAT THIS EXISTS TO FIX. `Path.exists`, `is_dir`, `is_file` and `is_symlink`
changed contract in CPython 3.14. Through 3.13 they answer False only when the
error from their own `stat`/`lstat` names the node's absence -- a private
allow-list, `_IGNORED_ERRNOS = (ENOENT, ENOTDIR, EBADF, ELOOP)`, plus three
Windows codes -- and every other `OSError` (a permission denial, an I/O error,
a stale handle) propagates. In 3.14 each one delegates to an `os.path`
function (`exists`, `lexists`, `isdir`, `isfile`, `islink`) that catches EVERY
`OSError` and answers False. So on 3.14 a node that cannot be read is
indistinguishable from a node that is not there.

That matters wherever the absent answer switches a check OFF. The #1201 survey
found such sites in `scripts/doc_health/`: the complete-coverage baseline gate,
the regression gate, the preflight validators, the pin-record ladder, the
aggregation-backlog detector and the catalog-tag guard each read "nothing
there" as "nothing to enforce", so on 3.14 an unreadable marker, report,
validator, record or directory would switch its gate off in silence. Brett
Heap's ruling on #1201 ("#1201: 1(b), raw OSError, add the 3.14 CI leg") routes
those sites through this module, with RAW `OSError` propagation: exactly what
3.12 and 3.13 do today.

WHAT THIS MODULE PROMISES. Every probe here is a single explicit `os.stat`
(following links) or `os.lstat` (not following) with the 3.12/3.13 allow-list
written out, so its answer is the SAME on every interpreter: on 3.12 and 3.13 a
call site that moves from `path.is_file()` to `fs_probe.is_file(path)` behaves
exactly as before, and on 3.14 it stops swallowing. `ValueError` (a path with
an embedded NUL byte, or one the filesystem encoding cannot represent) reads as
absent, as it does through 3.13.

WHAT IT DOES NOT DO. It never turns an error into a finding, a `Skip` or a
controlled refusal: the ruling chose raw propagation for these sites, so an
unreadable node crashes the run loudly, as it does on 3.12 today. The document
catalog's writer and scan (`catalog.py`) need a stricter, controlled flavour
-- absence is only `FileNotFoundError`/`NotADirectoryError`, and anything else
is a `CatalogError` naming the node tree-relative -- and keep their own
explicit `os.lstat` for it (`catalog._node_mode`).

Standard library only, so this leaf can be imported from anywhere in the
package without an import cycle.
"""

from __future__ import annotations

import errno
import os
import stat

#: The errnos CPython 3.12 and 3.13 pathlib read as "the node is not there"
#: (`pathlib._IGNORED_ERRNOS`): no such entry, a path component that is not a
#: directory, a bad descriptor, and a symlink loop. Any other errno propagates.
ABSENT_ERRNOS = frozenset({errno.ENOENT, errno.ENOTDIR, errno.EBADF,
                           errno.ELOOP})

#: The same allow-list's Windows half (`pathlib._IGNORED_WINERRORS`):
#: ERROR_NOT_READY (21), ERROR_INVALID_NAME (123) and
#: ERROR_CANT_RESOLVE_FILENAME (1921).
ABSENT_WINERRORS = frozenset({21, 123, 1921})


def _is_absence(exc: OSError) -> bool:
    return (getattr(exc, "errno", None) in ABSENT_ERRNOS
            or getattr(exc, "winerror", None) in ABSENT_WINERRORS)


def mode(path, *, follow_symlinks: bool = True) -> int | None:
    """``path``'s ``st_mode`` from one explicit ``os.stat`` (or ``os.lstat``
    with ``follow_symlinks=False``), or None when nothing is there. An
    ``OSError`` that does not name absence (``ABSENT_ERRNOS``) propagates
    unchanged, on every interpreter version."""
    try:
        if follow_symlinks:
            return os.stat(path).st_mode
        return os.lstat(path).st_mode
    except OSError as exc:
        if _is_absence(exc):
            return None
        raise
    except ValueError:
        return None  # an unrepresentable path, as pathlib reads it to 3.13


def exists(path, *, follow_symlinks: bool = True) -> bool:
    """``Path.exists`` with its 3.12/3.13 contract on every version."""
    return mode(path, follow_symlinks=follow_symlinks) is not None


def is_dir(path, *, follow_symlinks: bool = True) -> bool:
    """``Path.is_dir`` with its 3.12/3.13 contract on every version."""
    found = mode(path, follow_symlinks=follow_symlinks)
    return found is not None and stat.S_ISDIR(found)


def is_file(path, *, follow_symlinks: bool = True) -> bool:
    """``Path.is_file`` with its 3.12/3.13 contract on every version."""
    found = mode(path, follow_symlinks=follow_symlinks)
    return found is not None and stat.S_ISREG(found)


def is_symlink(path) -> bool:
    """``Path.is_symlink`` with its 3.12/3.13 contract on every version."""
    found = mode(path, follow_symlinks=False)
    return found is not None and stat.S_ISLNK(found)
