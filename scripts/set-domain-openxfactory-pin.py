#!/usr/bin/env python3
"""Set the openxFactory contract pin in DomainxFactory stack.yaml files.

This updater is intentionally text-preserving. It replaces only the top-level
`xfactory:` block so existing YAML layout elsewhere in the file does not churn.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v[0-9]+\\.[0-9]+\\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
TOP_LEVEL_RE = re.compile(r"^[A-Za-z0-9_]+:\s*$")


def infer_ref_type(ref: str) -> str:
    if SHA_RE.match(ref):
        return "commit"
    if TAG_RE.match(ref):
        return "tag"
    raise ValueError("openxFactory ref must be a 40-character SHA or vX.Y.Z tag")


def find_block(lines: list[str], key: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        if line == f"{key}:\n" or line == f"{key}:":
            start = index
            break
    if start is None:
        raise ValueError(f"missing top-level {key}: block")

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line.startswith((" ", "\t")) and TOP_LEVEL_RE.match(line):
            end = index
            break
    return start, end


PRESERVED_KEYS = ("promoted_from", "specializes")
SUB_KEY_RE = re.compile(r"^  [A-Za-z0-9_]+:")
# A comment line or a blank one: everything that carries no key and no value,
# and therefore everything whose meaning comes from what it is ATTACHED to.
COMMENT_OR_BLANK_RE = re.compile(r"^\s*(#.*)?$")


def preserved_subblocks(block: list[str]) -> list[str]:
    """Carry optional provenance sub-blocks through a pin rewrite verbatim —
    INCLUDING the comment lines attached to them.

    THE BUG THIS FIXES (found by `split-openxwallet-repo` P5a.2). The previous
    implementation kept a preserved key and its value lines and dropped every
    other line in the block, so the comment immediately ABOVE a preserved
    sub-block was regenerated away. In LedgerxFactory's `stack.yaml` those two
    lines read:

        # managed provenance (document-lifecycle promotion process) -- re-pin
        # tooling must preserve this block; regenerating it away is a health finding

    A tool that answers an instruction not to delete something by deleting the
    instruction is the worst available outcome: the next reader has no reason to
    think the block is protected, and the protection was never machine-readable
    in the first place. The comment is now preserved BY THE SAME RULE as the key
    it annotates.

    ATTRIBUTION RULE: a run of comment/blank lines belongs to what FOLLOWS it,
    which is the YAML convention and the one that makes the LedgerxFactory shape
    come out right. So the run is BUFFERED, not emitted on sight, and it is
    flushed only when a preserved key turns up next; a run followed by a
    non-preserved key (or by the end of the block) annotates something this
    rewrite is replacing and goes with it. That cuts both ways deliberately: the
    comment above `contract_source:` would be dropped, and should be, because
    the line it describes is regenerated from arguments on every run.

    A trailing run INSIDE a preserved sub-block's value lines is likewise held
    back rather than swallowed, so a comment sitting between the end of
    `promoted_from:`'s list and the next key is attributed to that next key
    instead of riding along with the list it merely follows.
    """
    kept: list[str] = []
    pending: list[str] = []
    index = 0
    while index < len(block):
        line = block[index]
        if COMMENT_OR_BLANK_RE.match(line):
            pending.append(line)
            index += 1
            continue
        if any(line.startswith(f"  {key}:") for key in PRESERVED_KEYS):
            kept.extend(pending)
            pending = []
            kept.append(line)
            index += 1
            trailing: list[str] = []
            while index < len(block) and not SUB_KEY_RE.match(block[index]):
                if COMMENT_OR_BLANK_RE.match(block[index]):
                    trailing.append(block[index])
                else:
                    # a real value line: whatever comments preceded it inside
                    # this sub-block belong to it, so they are no longer pending
                    kept.extend(trailing)
                    trailing = []
                    kept.append(block[index])
                index += 1
            pending = trailing
        else:
            # a regenerated key; its attached comments go with it
            pending = []
            index += 1
    return kept


def update_stack(path: Path, ref: str, ref_type: str, declared_at: str, source: str) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    start, end = find_block(lines, "xfactory")

    replacement = [
        "xfactory:\n",
        "  contract_repo: github.com/opensoft/openxFactory\n",
        "  contract_name: openxFactory\n",
        f"  contract_ref_type: {ref_type}\n",
        f"  contract_ref: {ref}\n",
        "  contract_schema_version: 1\n",
        f"  contract_declared_at: \"{declared_at}\"\n",
        f"  contract_source: {source}\n",
    ]
    replacement.extend(preserved_subblocks(lines[start + 1:end]))
    updated = "".join(lines[:start] + replacement + lines[end:])
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openxfactory-ref", required=True)
    parser.add_argument("--declared-at", default=date.today().isoformat())
    parser.add_argument("--source", default="xFactory-submodule-pin")
    parser.add_argument("domains", nargs="+", help="Domain repo directories or stack.yaml paths")
    args = parser.parse_args()

    ref_type = infer_ref_type(args.openxfactory_ref)
    for domain in args.domains:
        path = Path(domain)
        stack_path = path if path.name == "stack.yaml" else path / "stack.yaml"
        if not stack_path.exists():
            raise FileNotFoundError(stack_path)
        if update_stack(stack_path, args.openxfactory_ref, ref_type, args.declared_at, args.source):
            print(f"updated {stack_path}")
        else:
            print(f"ok {stack_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
