#!/usr/bin/env python3
"""Build § 5.2a's ADDED delta from the PROMOTED spec, title-keyed, and PROVE the carry.

Run from an openxFactory checkout root:
  python3 openspec/changes/repromote-engineering-vocabulary/review/build-delta.py . [--write]

It (1) selects the fifteen by the destination the packet's ratified map names for each
removed title, (2) lifts each requirement out of openspec/specs/ideation-dashboard/spec.md
by TITLE (never by line), (3) applies the TWO declared path-literal -> adapter-call edits,
each of which must match EXACTLY ONCE, and (4) proves every other byte is carried
identical by diffing the rebuilt block against the source with the edits reversed.
"""
import re, sys, difflib, hashlib
from pathlib import Path

CAP = "openxfactory-engineering-adapter"
CHANGE = "repromote-engineering-vocabulary"

# ---- the TWO declared edits: (requirement title, OLD, NEW, operation) ---------
# NARROWED 2026-09-16 after Copilot round 1 (threads 4029968885 and the suppressed
# comment on spec.md:42). Of the SIX path-literal occurrences in the fifteen, only
# these two name a question the seam's six operations actually answer — `resolve`,
# which design § D2 of the governing packet names for exactly this literal ("the
# operation `corpus_root.py` performs today with a path literal"). The other four
# are RECORDED NON-EDITS with their reasons in this packet's design.md § D2; a
# replacement there would be authoring, not re-expressing, and § 5.2a permits only
# the re-expression.
EDITS = [
 ("doxBench resolves its released contract from the checkout it runs in",
  "then the existing walk up to an aggregation-relative `openxFactory/`",
  "then the corpus adapter's `resolve` of the aggregation-relative home corpus",
  "resolve"),
 ("doxBench resolves its released contract from the checkout it runs in",
  "the hosting repository is a publisher release and an aggregation-relative `openxFactory/` checkout also exists",
  "the hosting repository is a publisher release and an aggregation-relative home corpus the adapter could resolve also exists",
  "resolve"),
]

def norm(title: str) -> str:
    """The corpus's own comparison spelling — `scripts/doc_health/promotion_fidelity.py`
    `norm()`, quoted rather than approximated: *"Whitespace-collapsed and
    casefolded, and NOTHING ELSE."* Re-implemented here because this helper
    imports nothing from the tree it verifies, and pinned by the guards below:
    every duplicate check in this file is keyed exactly the way the archive
    family keys `(capability, requirement)`, so a collision this build passes is
    not one that family would call a collision.
    """
    return " ".join(title.split()).casefold()


def _require_lf(path: Path) -> None:
    """Refuse a CR anywhere in a source this build reads.

    Extraction and the reversal proof compare TEXT, and `read_text()` applies
    universal-newline translation, so a source carrying CRLF would compare equal
    while the emitted delta was not byte-identical to it. This corpus is LF; a
    CR here is a fact worth refusing on rather than normalising past.
    """
    if b"\r" in path.read_bytes():
        raise _refuse(f"{path} carries a CR: this build compares text and would "
                      f"report a byte-identical carry it cannot guarantee.")


def requirements(text, path="<text>"):
    """(title -> body) for every '### Requirement:' block, in file order.

    Refuses a duplicate title rather than overwriting it — see the guard below.
    """
    lines = text.split("\n")
    idx = [(i, l[len("### Requirement: "):].strip())
           for i, l in enumerate(lines) if l.startswith("### Requirement: ")]
    out, seen = {}, {}
    for n, (i, t) in enumerate(idx):
        j = idx[n + 1][0] if n + 1 < len(idx) else len(lines)
        # FAIL CLOSED ON A DUPLICATE TITLE, KEYED THE WAY THE CORPUS KEYS.
        # `promotion_fidelity` keys on (capability, NORMALIZED title), so a
        # pair differing only in case or run-of-whitespace is ONE key there and
        # must be one here: a raw-string check would pass a collision the
        # archive family calls a collision. Overwriting silently would emit one
        # body twice under a title that means two things, and the reversal
        # proof would still pass. Refuse instead.
        if norm(t) in seen:
            raise _refuse(f"duplicate requirement title in {path}: {t!r} "
                          f"collides with {seen[norm(t)]!r} under the corpus's "
                          f"own normalization — the title-keyed selection this "
                          f"build performs cannot be trusted over it.")
        seen[norm(t)] = t
        out[t] = "\n".join(lines[i:j]).rstrip("\n")
    return out, [t for _, t in idx]

def _refuse(message: str) -> "SystemExit":
    """Every gate in this file raises; none of them asserts.

    `python3 -O` deletes `assert`, and a verifier whose gates vanish under a
    common interpreter flag is not a gate. The exact-once matching, the
    destination-map count, the title presence, the reversal proof and the
    committed-artifact comparison all come through here instead.
    """
    return SystemExit(f"REFUSED: {message}")


def main():
    root = Path(sys.argv[1]).resolve()
    write = "--write" in sys.argv
    packet = root / "openspec/changes/split-opendox-two-layer-product/specs/ideation-dashboard/spec.md"
    promoted = root / "openspec/specs/ideation-dashboard/spec.md"

    # (1) the fifteen, from the ratified map
    _require_lf(packet)
    pk = packet.read_text(encoding="utf-8")
    blocks = re.split(r"^### Requirement: ", pk, flags=re.M)[1:]
    fifteen, dest_count, all_titles = [], {}, []
    for b in blocks:
        title = b.split("\n", 1)[0].strip()
        all_titles.append(title)
        m = re.search(r"reads as \*\*(open[A-Za-z]+)", b)
        d = m.group(1) if m else "NOMATCH"
        dest_count[d] = dest_count.get(d, 0) + 1
        if d == "openxFactory":
            fifteen.append(title)
    dup = [t for t in set(map(norm, all_titles)) if list(map(norm, all_titles)).count(t) > 1]
    if dup:
        raise _refuse(f"the ratified map carries {len(dup)} duplicated title(s) "
                      f"under the corpus's normalization: {dup} — the row counts "
                      f"below would pass while a row was silently lost.")
    print(f"map: {dest_count}  (expect openDox 71 / openXdox 16 / openxFactory 15)")
    if dest_count != {"openDox": 71, "openXdox": 16, "openxFactory": 15}:
        raise _refuse(f"the destination map is not 71/16/15: {dest_count}")
    if len(fifteen) != 15:
        raise _refuse(f"the openxFactory column is {len(fifteen)}, not 15")

    # (2) lift by title from the promoted spec
    _require_lf(promoted)
    pr = promoted.read_text(encoding="utf-8")
    reqs, order = requirements(pr, promoted)
    print(f"promoted requirements: {len(order)}")
    missing = [t for t in fifteen if t not in reqs]
    if missing:
        raise _refuse(f"titles absent from the promoted spec: {missing}")
    wanted = {norm(t) for t in fifteen}
    if len(wanted) != len(fifteen):
        raise _refuse("the openxFactory column carries a normalized-title "
                      "duplicate; the ordered selection would silently shrink.")
    fifteen = [t for t in order if norm(t) in wanted]      # promoted-file order
    if len(fifteen) != 15:
        raise _refuse(f"the ordered selection is {len(fifteen)}, not 15 — a "
                      f"title in the map does not match one in the promoted spec")
    carried = {t: reqs[t] for t in fifteen}
    src_bytes = sum(len(carried[t].encode()) for t in fifteen)
    scen = sum(carried[t].count("#### Scenario:") for t in fifteen)
    print(f"carried: {len(fifteen)} requirements, {src_bytes} source bytes, {scen} scenarios")

    # (3) the two edits, each exactly once
    edited = dict(carried)
    for title, old, new, klass in EDITS:
        if title not in edited:
            raise _refuse(f"edit names a requirement not carried: {title!r}")
        n = edited[title].count(old)
        if n != 1:
            raise _refuse(f"edit matched {n}x (expected exactly 1): "
                          f"{title!r} :: {old[:60]}")
        edited[title] = edited[title].replace(old, new)
        print(f"  edit [{klass}] in {title[:52]!r}: OK")

    # (4) prove nothing else moved: reverse the edits, expect byte equality
    for t in fifteen:
        back = edited[t]
        for title, old, new, _ in EDITS:
            if title == t:
                back = back.replace(new, old)
        if back != carried[t]:
            raise _refuse(
                f"BYTES MOVED outside the declared edits in: {t}\n" +
                "\n".join(difflib.unified_diff(carried[t].split("\n"),
                                                back.split("\n"), lineterm="", n=1)))
    print("REVERSAL PROOF: every byte outside the two declared edits is carried identical.")

    body = []
    for t in fifteen:
        body.append(edited[t])
    delta = HEADER + "\n\n## ADDED Requirements\n\n" + "\n\n".join(body) + "\n"
    out = root / f"openspec/changes/{CHANGE}/specs/{CAP}/spec.md"
    digest = hashlib.sha256(delta.encode()).hexdigest()
    print(f"delta: {len(delta.encode())} bytes, sha256 {digest[:16]}…")
    if write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(delta, encoding="utf-8")
        print(f"WROTE {out.relative_to(root)}")
        return

    # (5) WITHOUT --write THIS IS A CHECK, NOT A DRY RUN. Rebuilding in memory and
    # printing a hash would pass over a committed delta somebody had edited by
    # hand, which is exactly the artifact the archive promotes. So the committed
    # file is READ and compared, and a mismatch or an absence is a non-zero exit.
    if not out.exists():
        raise SystemExit(f"CHECK FAILED: {out.relative_to(root)} does not exist; "
                         f"re-run with --write to author it.")
    # BYTES, NOT TEXT. `read_text()` applies universal-newline translation, so a
    # committed delta whose line endings had been changed would read back equal
    # and pass a str comparison. The guard exists to catch exactly that class.
    committed = out.read_bytes()
    if committed != delta.encode("utf-8"):
        diff = "\n".join(list(difflib.unified_diff(
            committed.decode("utf-8", "replace").split("\n"), delta.split("\n"),
            fromfile="committed", tofile="rebuilt", lineterm=""))[:40])
        raise SystemExit("CHECK FAILED: the committed delta is not what this build "
                         f"produces (byte comparison).\n{diff}")
    print(f"CHECK PASSED: {out.relative_to(root)} is byte-identical to this build "
          f"({len(committed)} bytes, sha256 {digest[:16]}…).")

HEADER = f"""# {CAP} Specification

This delta is the RE-PROMOTION half of `split-opendox-two-layer-product` § 5.2a: the
FIFTEEN engineering-vocabulary requirements that leave the capability
`ideation-dashboard` and STAY IN THIS REPOSITORY under **RULING DQ-1**
(`opensoft/openxFactory` issue #656, 2026-09-04T22:14Z, comment `5547049745`) land here,
under the successor capability of the adapter § 2.2a stood up — one conformant
implementation of openDox's corpus-adapter seam over this repository's own corpus,
`scripts/corpus_adapter_openxfactory/`, landed by #725 → `ea4e6ff2`.

**THE FIFTEEN ARE NOT AUTHORED HERE; THEY ARE CARRIED.** Each requirement below was
lifted from `openspec/specs/ideation-dashboard/spec.md` BY TITLE rather than by line or
by hand, and carries every byte of its promoted text except at the TWO sites
`design.md` § D2 discloses, where a path literal becomes the seam operation that answers
for it. The other FOUR path-literal occurrences in the fifteen are RECORDED NON-EDITS,
each with its reason: no operation of the six-wide seam answers the question its
requirement asks at those words, and replacing a literal with prose that names no call
would be authoring rather than re-expressing.

Titles are therefore character-for-character identical to the promoted spec — the
same discipline the packet's own removal block states for the same reason:
`scripts/doc_health/promotion_fidelity.py` keys on (capability, normalized title), so
the successor is a DISTINCT key, this re-promotion masks nothing, and the packet's
`## REMOVED` delta stays visible to the checker.

**THIS DELTA REMOVES NOTHING.** The departure from `ideation-dashboard` is the packet's
own ratified per-requirement map — 71 openDox / 16 openXdox / 15 openxFactory, ratified
2026-09-05T01:38Z — and that map is the single writer of the removal. See `design.md`
§ D3 for why a second `## REMOVED` block over the same fifteen titles is refused here.

## Purpose

Carry the requirements of `openxFactory`'s OWN ENGINEERING ADAPTER — the one
conformant implementation of openDox's corpus-adapter seam that reads THIS
repository's corpus, and the engineering mapping it serves: staged topics and
their health, the promotion funnel to proposal, the possibles register, the
reverse transition that demotes a change back to its topic, the register-edit
fulfilment lane, and the released-contract resolution the runtime performs
before it serves any of them. RULING DQ-1 (`opensoft/openxFactory` issue #656,
2026-09-04T22:14Z) kept that adapter and that vocabulary HERE when the
document-and-ideation workbench left: these fifteen requirements are the part of
`ideation-dashboard` that did not travel, and they state what this repository's
own gate console, its reverse transitions and its runtime must do over a corpus
reached THROUGH the seam rather than through a path literal.

The seam itself is NOT this capability. The interface is openDox's under RULING
Q4, declared as `corpus-adapter-seam`; this capability holds one implementation's
obligations under it, and under that interface's fourth requirement it is one
implementation among others with no privileged route to its home corpus."""

main()
