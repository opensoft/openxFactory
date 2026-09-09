#!/usr/bin/env python3
"""A pin's REGISTRATION is checked: path, consumer entrypoint and rule agree.

THE GAP THIS CLOSES (issue #776, second assertion).
`publish-openspec-cli-pin-as-contract-member` registered one consumption pin in
`contracts/manifest.yaml` and wrote NO CHECK — its own `tasks.md` § 5.4 says so
in its heading: *a registration is not a check*. The registered row's
`consumption_rule` QUOTES a path (`scripts/validate-openspec-cli-pin.py`); the
pin file NAMES that same path in its own `consumer_entrypoint:` field; and
nothing in this repository compared the two. `design.md` D2 carried that
coupling as DISCLOSED. The only comparison of `consumer_entrypoint:` against
anything in the tree — `tests/proposal-support/test_pinned_openspec_cli.py` —
compares `proposal-support`'s own constant against the PIN, never the MANIFEST
ROW against the pin, and stays green through exactly the failure this file
exists to catch.

THE FAILURE MODE, NAMED. A rename that moved the entrypoint and updated the pin
but not the row's prose — or moved the pin and not the row — leaves the
PUBLISHED register quoting a path that does not exist, silently, to precisely
the audience the register exists for: a cross-repository consumer reading
`contracts/manifest.yaml` to learn how to consume. Declining the row's `sha256`
(D2's stated choice, because the pin moves on every disposition added or
retired) did not remove that coupling; it made it ONE STRING wide instead of one
file wide, and one string is still uncompared.

WHAT CANON REQUIRES, AND NOTHING MORE. `openspec/specs/neutral-product-pin/`'s
promoted requirement *A consumption pin that another repository reads is a
PUBLISHED contract member, adopted by pin-sync* obliges the registration to
carry "an `id`, its `path`, a `type`, its `intended_consumers`,
`adapter_owner: openxFactory`, and a `consumption_rule` that states the
checkout-at-the-pinned-ref recipe"; it fixes the recipe as "check `openxFactory`
out at its own `stack.yaml` `xfactory.contract_ref` and invoke the entrypoint
the registered pin names FROM THAT CHECKOUT"; and it holds that "WHERE THE TWO
GOVERNED ACTS ARE REACHED BY TWO DIFFERENT COMMANDS, THE REGISTER SHALL NAME
BOTH … published adoption instructions SHALL name the ACTUAL command for each
governed act they cover". Its own scenario for an unexecutable instruction is
that "a consumer following it literally falls back to the ambient tool", which
is the state the pin exists to end. The three assertions below are those
sentences and no further rule.

WHAT THIS FILE DELIBERATELY DOES NOT ASSERT. Issue #776's FIRST assertion —
that a pin some OTHER repository reads IS registered at all — needs a machine
test for "is read", which canon does not carry and which that issue leaves
explicitly unpicked (read the pin's `intended_consumers`, read the row's, take
the union, or require the pin to declare its own answer, "all defensible and all
have costs"). Choosing one is a governed act, not a plain fix, so this checker
walks the REGISTERED rows and asks only whether each is internally coherent. The
two pin files that sit unregistered on `main` are the sibling question, filed
separately as issue #775, and this file neither answers nor forecloses it.

WHY A CHECKER OF ITS OWN, BESIDE THE FAMILIES RATHER THAN INSIDE ONE. § 5.4
placed it beside `release-inventory-drift` rather than in it: that family grades
whether the derived release membership has drifted from the declared bundle — a
different question from whether the consumption register is internally coherent
— and folding two questions into one family makes the finding text unable to say
which failed. The same sentence rules out folding it into
`scripts/validate-manifest-digests.py`, whose docstring scopes itself to rows
CARRYING a `sha256` and declares rows without one "out of scope by design" — and
a pin row has no `sha256`, by D2's deliberate choice. And it rules out adding it
to `scripts/validate-openspec-cli-pin.py`, which is vendored BYTE-IDENTICAL into
three sibling repositories: a check added there grows the re-vendor debt for a
question that is openxFactory's alone. Neither the pin file nor that vendored
validator is touched by this change.

TWO SHARPENINGS TAKEN FROM THE REVIEW BENCH, both of them the same defect class
this file is about — a comparison that passes without measuring. Copilot and
Codex each raised that `ROOT / <claimed>` DISCARDS the root for an absolute path
and follows a `..` out of the tree, so a row naming a host path would be
reported "in this tree" whenever the HOST carries that file while no consumer's
checkout does; `resolve_in_tree` refuses both, mirroring
`scripts/validate-avatar-client.py`'s containment helper and Article IV's
"Committed files MUST NOT contain host-absolute paths". Codex raised that a bare
substring test reports `scripts/tool.py.old` as naming `scripts/tool.py` — the
exact rename drift this lane exists to catch, passing; `rule_names_entrypoint`
requires a delimited path token.

Run: python3 scripts/validate-pin-registrations.py (also exercised by
tests/pin_registrations/test_pin_registration_sweep.py on every required-suite
pass, the same lane `tests/manifest_digests/` gives the estate-wide digest
sweep, so the checker IS run rather than merely runnable).
Exit codes: 0 every registered pin coheres, 1 named findings, 2 harness error.
"""
from __future__ import annotations

import string
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts" / "manifest.yaml"

PIN_TYPE = "pin"
ENTRYPOINT_FIELD = "consumer_entrypoint"
RULE_FIELD = "consumption_rule"

# A path token continues across these; a delimited occurrence of the entrypoint
# is one that neither of them runs into. See `rule_names_entrypoint` below.
NAME_CHARS = frozenset(string.ascii_letters + string.digits + "._-")
TRAILING_CHARS = NAME_CHARS | frozenset("/")


def resolve_in_tree(claimed):
    """The claimed path resolved inside `ROOT`, or a REFUSAL REASON.

    Returns `(path, None)` or `(None, reason)`. Mirrors
    `scripts/validate-avatar-client.py`'s containment helper rather than
    inventing a second dialect for the same question, and exists because
    `Path(root) / "/abs"` DISCARDS the root: a row naming an absolute or
    `..`-escaping path would otherwise be reported "in this tree" whenever the
    HOST happens to carry that file, while no consumer's checkout contains it.
    The constitution's Article IV says the same thing about the corpus —
    "Committed files MUST NOT contain host-absolute paths; use repo-relative
    paths or runtime resolution" — so a register naming one is a finding on its
    own terms and not merely an unreadable path.
    """
    if not isinstance(claimed, str) or not claimed.strip():
        return None, ("is not a non-empty string path, and `ROOT / "
                      "<non-string>` raises rather than reporting")
    candidate = Path(claimed)
    if candidate.is_absolute():
        return None, ("is an ABSOLUTE path; joining one to the repository root "
                      "discards the root entirely, and no consumer's checkout "
                      "carries a host path")
    if ".." in candidate.parts:
        return None, ("contains a '..' segment, which walks out of the "
                      "repository the register speaks for")
    root = ROOT.resolve()
    target = (root / candidate).resolve()
    if not target.is_relative_to(root):
        return None, (f"resolves to {target}, which is outside the repository; "
                      f"refused rather than read")
    return target, None


def rule_names_entrypoint(rule: str, entrypoint: str) -> bool:
    """True when `rule` names `entrypoint` as a DELIMITED path token.

    A bare substring test is too weak for the drift this lane exists to catch:
    a stale rule saying `scripts/tool.py.old` CONTAINS `scripts/tool.py`, so the
    rename that produced it would be reported coherent. An occurrence therefore
    counts only when the text does not continue the token — a following name
    character, `.`, `-`, `_` or `/` all mean the rule is naming a DIFFERENT
    path.

    A LEADING `/` is deliberately allowed while a leading name character is not:
    `.openxfactory-pin/scripts/tool.py` is the same entrypoint named through the
    checkout directory a consumer is told to make, which is exactly the recipe
    the register publishes, whereas `myscripts/tool.py` is another file.
    """
    start = 0
    while True:
        index = rule.find(entrypoint, start)
        if index == -1:
            return False
        before = rule[index - 1] if index else ""
        end = index + len(entrypoint)
        after = rule[end] if end < len(rule) else ""
        if before not in NAME_CHARS and after not in TRAILING_CHARS:
            return True
        start = index + 1


def iter_pin_rows(node):
    """Every mapping registering `type: pin`, wherever it sits in the manifest.

    The walk is recursive on `validate-manifest-digests.py`'s precedent rather
    than indexing `contracts:` directly, so a row nested under a future grouping
    key is still measured instead of silently unmeasured.
    """
    if isinstance(node, dict):
        if node.get("type") == PIN_TYPE:
            yield node
        for value in node.values():
            yield from iter_pin_rows(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_pin_rows(item)


def check_row(row, findings):
    """Append a named finding per failed assertion; return True if the row is ok.

    Every assertion is reported independently: a row can fail more than one, and
    a reader who is told only the first has to re-run to learn the rest.
    """
    row_id = str(row.get("id", "<row with no id>"))
    ok = True

    raw_path = row.get("path")
    if not raw_path:
        findings.append(
            f"FAIL {row_id}: registered as `type: {PIN_TYPE}` but the row carries "
            f"no `path`, so the register names no pin at all")
        return False

    pin_path, refusal = resolve_in_tree(raw_path)
    if refusal is not None:
        findings.append(
            f"FAIL {row_id}: the row registers `{raw_path}`, which {refusal} — "
            f"a register naming a path outside the tree publishes bytes no "
            f"consumer's checkout contains")
        return False

    if not pin_path.is_file():
        findings.append(
            f"FAIL {row_id}: the row registers `{raw_path}` but no such file is "
            f"in this tree — the register publishes a pin a consumer cannot read")
        return False

    try:
        pin = yaml.safe_load(pin_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        findings.append(
            f"FAIL {row_id}: the pin at `{raw_path}` is registered but does not "
            f"parse as YAML ({exc.__class__.__name__}), so nothing can be "
            f"compared against it")
        return False

    if not isinstance(pin, dict):
        findings.append(
            f"FAIL {row_id}: the pin at `{raw_path}` is registered but is not a "
            f"YAML mapping, so it names no `{ENTRYPOINT_FIELD}:` to compare")
        return False

    entrypoint = pin.get(ENTRYPOINT_FIELD)
    if entrypoint is None:
        # A pin that names no entrypoint reaches neither of the two assertions
        # below, and canon obliges no pin to carry the field. Reported as
        # measured rather than passed over in silence, so a reader can tell an
        # inapplicable assertion from an unmade one.
        print(f"OK {row_id}: `{raw_path}` is registered and present; it names no "
              f"`{ENTRYPOINT_FIELD}:`, so the entrypoint assertions do not apply")
        return True

    entrypoint = str(entrypoint)
    entrypoint_path, refusal = resolve_in_tree(entrypoint)
    if refusal is not None:
        findings.append(
            f"FAIL {row_id}: the pin names `{ENTRYPOINT_FIELD}: {entrypoint}`, "
            f"which {refusal} — the published recipe invokes the entrypoint FROM "
            f"THE PINNED CHECKOUT, and a path outside it is unreachable there")
        ok = False
    elif not entrypoint_path.is_file():
        findings.append(
            f"FAIL {row_id}: the pin names `{ENTRYPOINT_FIELD}: {entrypoint}` but "
            f"no such file is in this tree — a consumer following the published "
            f"recipe literally gets a missing-file error and falls through to the "
            f"ambient tool, the state the pin exists to end")
        ok = False

    rule = row.get(RULE_FIELD)
    if rule is None:
        findings.append(
            f"FAIL {row_id}: the row carries no `{RULE_FIELD}`, so it names no "
            f"command for any governed act while the pin names "
            f"`{entrypoint}` — the register must state the "
            f"checkout-at-the-pinned-ref recipe")
        ok = False
    elif not rule_names_entrypoint(str(rule), entrypoint):
        findings.append(
            f"FAIL {row_id}: the row's `{RULE_FIELD}` never names `{entrypoint}` "
            f"as a whole path — a longer path that merely CONTAINS it is a "
            f"different file and is exactly the rename drift this asks about; "
            f"the entrypoint this pin's `{ENTRYPOINT_FIELD}:` field carries — the "
            f"register must name the ACTUAL command for each governed act, and a "
            f"rule that names none is not executable by the consumer it is "
            f"published for")
        ok = False

    if ok:
        print(f"OK {row_id}: `{raw_path}` is present, its "
              f"`{ENTRYPOINT_FIELD}: {entrypoint}` resolves, and the row's "
              f"`{RULE_FIELD}` names that same path")
    return ok


def main() -> int:
    if not MANIFEST.is_file():
        print(f"ERROR {MANIFEST} is missing: the consumption register is the "
              f"surface this checker reads, and its absence is a harness error "
              f"rather than a clean corpus", file=sys.stderr)
        return 2
    try:
        doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR {MANIFEST} does not load ({exc.__class__.__name__}): the "
              f"register cannot be read, which is a harness error and never an "
              f"empty pass", file=sys.stderr)
        return 2

    findings: list[str] = []
    rows = list(iter_pin_rows(doc))
    for row in rows:
        check_row(row, findings)

    for finding in findings:
        print(finding)
    if findings:
        print(f"FAIL {len(findings)} finding(s) over {len(rows)} pin "
              f"registration(s) in contracts/manifest.yaml")
        return 1
    print(f"OK contracts/manifest.yaml: {len(rows)} pin registration(s) cohere")
    return 0


if __name__ == "__main__":
    sys.exit(main())
