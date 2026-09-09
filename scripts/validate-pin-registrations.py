#!/usr/bin/env python3
"""A pin's REGISTRATION is checked: path, entrypoint, rule — and its citations.

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

AND THEN THE SAME DEFECT CLASS ARRIVED INSIDE THE PIN (issue #840, the fourth
assertion). A `dispositions[]` entry ACCEPTS one ERROR-level finding of the
pinned tool, and the pin's header rests the whole mechanism on one sentence:
"A DISPOSITION WITHOUT A CITATION IS REFUSED, not ignored … `cited_to:` is
required and must be non-empty", because "an uncited exception is the thing this
estate refuses everywhere else it appears". `validate-openspec-cli-pin.py`
enforces that the field is a non-empty list, PRINTS its members in the
disposition report a reviewer reads — and never opens one. PR #834 renamed a
change directory; two citations in the live pin went on naming
`prepare-openspec-1.12-readiness`; `--all --no-cache` exited 0 before and after;
and the drift was caught by a human reading a diff. That is this file's own
failure mode one level down — a value the register publishes and nothing
compares — so it is this file's fourth assertion rather than a new checker.
`check_citations` and `classify_citation` carry the reasoning, the grammar the
pin actually documents, and the four things the arm deliberately does not assert.

Run: python3 scripts/validate-pin-registrations.py (also exercised by
tests/pin_registrations/test_pin_registration_sweep.py on every required-suite
pass, the same lane `tests/manifest_digests/` gives the estate-wide digest
sweep, so the checker IS run rather than merely runnable).
Exit codes: 0 every registered pin coheres, 1 named findings, 2 harness error.
`WARN` lines report a thing MEASURED that this file may not repair — they name
it, and they do not move the exit code.
"""
from __future__ import annotations

import re
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
DISPOSITIONS_FIELD = "dispositions"
CITATION_FIELD = "cited_to"

# The citation grammar, as the pin's own header and its own reader document it —
# and NOT one character more. See `classify_citation`.
#
# `—` (EM DASH) separates a citation's REFERENT from the prose gloss that says
# why it is cited; every citation in the live pin is written that way.
# `§` introduces a section inside the referent's document.
# A trailing parenthetical is an aside about the referent (`codexFactory PR #216
# (prepare-openspec-1.12-readiness, head b2a6af34)`), never part of it.
CITATION_GLOSS = "\u2014"
CITATION_SECTION = "\u00a7"
_TRAILING_PAREN = re.compile(r"\((?:[^()]*)\)\s*$")
_LINE_SUFFIX = re.compile(r"^(?P<path>.+?)(?::(?P<line>\d+))?$")
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")

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


def as_citation_text(citation):
    """The citation LINE the pin's own reader sees, or `None`.

    THE TWO GRAMMARS DISAGREE, MEASURED ON THE LIVE PIN. This checker reads the
    pin through `yaml.safe_load`; the pin's own verifier reads it with a
    line-based reader whose `cited_to` production is `^      - (\\S.*)$` — the
    WHOLE remainder of the line, verbatim, as one citation string. Two of the
    live pin's citations quote the tool's own output inside them (```Totals: 23
    passed, 2 failed (25 items)```), and a bare `: ` inside a YAML plain scalar
    makes it a SINGLE-KEY MAPPING to every general YAML parser. So the same two
    lines are one string to the pin's reader and `{key: value}` here, and a
    checker that only knew its own parser would report the pin's own citations
    unreadable while the pin reads them fine.

    A single-key mapping is therefore RECONSTRUCTED as `f"{key}: {value}"`,
    which restores the line byte for byte (PyYAML consumed exactly the `: `
    separator), and the reconstruction is what gets classified — so this arm
    reads the citation the pin reads. Anything else (a list, a number, a
    multi-key mapping) is not recoverable and comes back `None`.
    """
    if isinstance(citation, str):
        return citation
    if isinstance(citation, dict) and len(citation) == 1:
        (key, value), = citation.items()
        if isinstance(key, str):
            return f"{key}: {value}"
    return None


def classify_citation(citation):
    """What ONE `cited_to:` entry names, and whether this tree can resolve it.

    Returns `(kind, referent)`. `kind` is one of:

      * `"tree-path"`   — an UNQUALIFIED repo-relative path; this tree resolves it
      * `"url"`         — an absolute URL, resolved by the network and not here
      * `"reference"`   — `#N` or `owner/repo#N`, resolved by a forge and not here
      * `"qualified"`   — a path a QUALIFIER puts in some other context (the live
                          pin's `codexFactory openspec/changes/…/spec.md`); this
                          tree is not the tree it names, so it is not resolved
      * `"prose"`       — no machine referent at all (`council LA-A1`)
      * `"unreadable"`  — not a non-empty string

    THE GRAMMAR THIS FOLLOWS IS THE ONE THE PIN DOCUMENTS, AND THAT GRAMMAR IS
    THIN. `contracts/openspec-cli-pin.yaml`'s header says of the field exactly
    this much — "`cited_to:` is required and must be non-empty" — and its own
    reader, `scripts/validate-openspec-cli-pin.py`, admits it as a nested list of
    non-empty string lines (`_SEQ_MAP_LIST_ITEM`) whose members it never parses,
    on the stated ground that "flattening them into one delimited string would
    make the reader guess a delimiter that a citation could itself contain". So a
    citation is prose that may CONTAIN a machine referent, and there is no
    declared grammar saying which. This function therefore reads a referent only
    where the citation names one unambiguously, and every other form comes back
    as recognised-but-not-resolved rather than as a finding: enforcing a
    reference grammar canon does not carry would make this checker the author of
    a rule instead of the reader of one, which is the failure `check_row`'s
    docstring already refuses under "WHAT CANON REQUIRES, AND NOTHING MORE".

    THE READING, IN ORDER. The gloss after the em dash is cut; a `§` section and
    a trailing parenthetical are cut with it; the LAST remaining token is the
    referent, because the live pin's own form is `<qualifiers> <referent> — <why
    it is cited>` and one citation names one act (a second act is a second list
    entry, which is why the field is a list at all).

    A QUALIFIER MAKES A PATH FOREIGN, deliberately and visibly. `codexFactory
    openspec/changes/…` is codexFactory's path, and this tree neither carries it
    nor may report it missing; an unqualified `openspec/specs/…` is this
    repository's, which is the form every in-tree citation in the live pin uses.
    A citation that puts any word before its path has told the reader to read it
    somewhere else, so it is returned `"qualified"` and COUNTED in the output —
    an unresolved citation is stated, never passed over, so the count itself
    tells a reader how much was measured.

    A `#` OR A `://` MEANS THE REFERENT IS NOT A PATH. `PR #444`, `#673` and
    `owner/repo#12` are forge references and `https://…` is a URL; each names
    something outside the tree, and reading any of them as a path would report
    every one of them missing.
    """
    if not isinstance(citation, str) or not citation.strip():
        return "unreadable", citation
    head = citation.split(CITATION_GLOSS, 1)[0]
    head = head.split(CITATION_SECTION, 1)[0]
    head = _TRAILING_PAREN.sub("", head).strip()
    tokens = head.split()
    if not tokens:
        # The citation is a gloss and nothing else: `— the measurement`. There is
        # no referent to resolve, and inventing one would be a guess.
        return "prose", head
    referent = tokens[-1].strip("`'\"" + CITATION_SECTION)
    if _URL_SCHEME.match(referent):
        return "url", referent
    if "#" in referent:
        return "reference", referent
    if "/" not in referent:
        # Every path citation in this corpus names a directory, and a bare
        # dotted token is as likely to be a version (`1.12.0`) or a change id
        # (`prepare-openspec-1-12-readiness`) as a filename — so a referent
        # naming no directory is not read as a path.
        return "prose", referent
    match = _LINE_SUFFIX.match(referent)
    # The `:1770` suffix is a READING AID and the FILE is the referent: it is
    # stripped and NOT checked, because a line number drifts with every edit
    # above it, and a checker that failed on that would report a finding on
    # unrelated insertions while the citation still names the right document.
    # The pin's header documents no line grammar to enforce either way.
    claimed = (match.group("path") if match else referent).rstrip(",;")
    if len(tokens) > 1:
        return "qualified", claimed
    return "tree-path", claimed


def check_citations(row_id, raw_path, pin, findings):
    """Every `dispositions[].cited_to` path resolves; return True if all do.

    THE GAP THIS CLOSES (issue #840). A disposition is an ACCEPTED EXCEPTION to a
    pinned tool's judgment, and the pin's header states the whole of what makes
    one lawful: "A DISPOSITION WITHOUT A CITATION IS REFUSED, not ignored …
    `cited_to:` is required and must be non-empty", on the ground that "an
    uncited exception is the thing this estate refuses everywhere else it
    appears". `scripts/validate-openspec-cli-pin.py` enforces that the field is
    a non-empty list and PRINTS its members in the disposition report a reviewer
    reads — and it never opens one. So a citation could name a path that no
    longer exists and every run would still exit 0, which is the state PR #834
    produced by renaming a change directory: two citations in the live pin went
    on naming `prepare-openspec-1.12-readiness`, the entrypoint's `--all
    --no-cache` run exited 0 before and after, and the drift was found by a
    reviewer reading a diff rather than by anything that asks. A citation nobody
    can open is a suppression with a footnote, and the footnote is the only
    difference the header rests the mechanism on.

    WHAT IT ASSERTS. For each `dispositions[]` entry of the registered pin, each
    `cited_to` member is classified by `classify_citation`; the members that name
    an UNQUALIFIED repo-relative path are resolved inside this tree with the same
    containment helper the registered `path` and `consumer_entrypoint:` go
    through, and a path that is absent — or absolute, or `..`-escaping — is a
    named finding and exit 1. `.exists()` and not `.is_file()`, because a
    citation legitimately names a change packet's directory.

    WHAT IT DELIBERATELY DOES NOT ASSERT. Not the `:<line>` suffix (above). Not
    a URL's reachability, a forge reference's existence, or another repository's
    path: this checker reads one tree and says so, and a network or a sibling
    checkout is not in it. Not `cited_to:`'s presence or shape — the pin's own
    verifier refuses that as `pin-disposition-malformed`, in its own words, and
    restating another checker's refusal in different words is what § 5.4 refused
    when it kept these questions in separate families. Not `dispositions[].path`,
    which the entrypoint reconciles against the tool's report and which this
    checker has no report to compare against.
    """
    dispositions = pin.get(DISPOSITIONS_FIELD)
    if dispositions is None:
        print(f"OK {row_id}: `{raw_path}` carries no `{DISPOSITIONS_FIELD}:`, so "
              f"the citation assertion does not apply")
        return True
    if not isinstance(dispositions, list) or not dispositions:
        print(f"OK {row_id}: `{raw_path}` records "
              f"`{DISPOSITIONS_FIELD}: {dispositions!r}`, which carries no entry "
              f"to read a citation from; the pin's own verifier owns that "
              f"refusal (`pin-disposition-malformed`) and it is not restated here")
        return True

    ok = True
    counts = {"tree-path": 0, "url": 0, "reference": 0, "qualified": 0,
              "prose": 0}
    total = 0
    uncited = 0
    recovered = 0
    for index, entry in enumerate(dispositions, start=1):
        where = f"{DISPOSITIONS_FIELD}[{index}]"
        if not isinstance(entry, dict):
            # A bare value is `pin-disposition-malformed` to the pin's own
            # verifier, in its own words. Counted as carrying no citation rather
            # than re-reported here.
            uncited += 1
            continue
        item = str(entry.get("item", "unnamed"))
        citations = entry.get(CITATION_FIELD)
        if not isinstance(citations, list) or not citations:
            uncited += 1
            continue
        for citation in citations:
            total += 1
            text = as_citation_text(citation)
            if text is None:
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) records the citation "
                    f"{citation!r}, which is neither a string nor a single-key "
                    f"mapping this arm can reconstruct into the line the pin's "
                    f"own reader sees — nothing about it can be read, let alone "
                    f"opened")
                ok = False
                continue
            if not isinstance(citation, str):
                # NOT a finding, and the reason is written down. In the pin's OWN
                # grammar the line is a well-formed citation — its reader takes
                # the whole line — so the defect is that the file's bytes mean
                # two different things to two readers, and the fix (quoting the
                # scalar) changes what that line-based reader CAPTURES, in a file
                # vendored byte-identical into three sibling repositories. That
                # is a governed repair with a re-vendor cost, not a path this
                # plain fix may take, so it is REPORTED here and named for a
                # successor rather than silently passed or silently forced.
                recovered += 1
                print(f"WARN {row_id}: {where} ({item}) carries a citation that "
                      f"`yaml.safe_load` reads as a single-key MAPPING and the "
                      f"pin's own line-based reader reads as one string — a bare "
                      f"`: ` inside the quoted tool output makes the two grammars "
                      f"disagree about the same bytes. Reconstructed and "
                      f"classified as the pin reads it; quoting it is a separate "
                      f"act, because the pin's reader captures the whole line "
                      f"INCLUDING the quotes and that reader is vendored into "
                      f"three sibling repositories")
            kind, referent = classify_citation(text)
            if kind == "unreadable":
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) records the citation "
                    f"{citation!r}, which is not a non-empty string — the pin "
                    f"admits one citation per line and nothing about it can be "
                    f"read, let alone opened")
                ok = False
                continue
            if kind != "tree-path":
                counts[kind] += 1
                continue
            counts["tree-path"] += 1
            target, refusal = resolve_in_tree(referent)
            if refusal is not None:
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) cites `{referent}`, which "
                    f"{refusal} — a citation is opened from the pinned checkout, "
                    f"and a path outside it is unreadable there")
                ok = False
                continue
            if not target.exists():
                findings.append(
                    f"FAIL {row_id}: {where} ({item}) cites `{referent}`, but no "
                    f"such path is in this tree — a disposition rests on its "
                    f"citation, and a citation a reader cannot open is a "
                    f"suppression with a footnote")
                ok = False

    measured = (f"{counts['tree-path']} name a path in this tree, "
                f"{counts['url']} a URL, {counts['reference']} a forge "
                f"reference, {counts['qualified']} a path qualified to another "
                f"repository, {counts['prose']} no machine referent")
    if recovered:
        measured += (f"; {recovered} reconstructed from a single-key mapping "
                     f"`yaml.safe_load` and the pin's own reader disagree about, "
                     f"warned above")
    if uncited:
        measured += (f"; {uncited} disposition(s) carry no `{CITATION_FIELD}:` "
                     f"list, which the pin's own verifier refuses as "
                     f"`pin-disposition-malformed`")
    if ok:
        print(f"OK {row_id}: {len(dispositions)} disposition(s) carry {total} "
              f"citation(s) — {measured}; every in-tree path resolves")
    else:
        print(f"MEASURED {row_id}: {len(dispositions)} disposition(s) carry "
              f"{total} citation(s) — {measured}")
    return ok


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
            f"FAIL {row_id}: the row registers `{raw_path!r}`, which {refusal} — "
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

    # THE CITATION ARM RUNS FIRST, and unconditionally, because the entrypoint
    # assertions below are terminal for a row on their own refusals: reaching
    # this question afterwards would mean a pin whose `consumer_entrypoint:` is
    # unreadable hides every dangling citation it carries behind that one
    # finding, and a reader told only the first has to re-run to learn the rest.
    citations_ok = check_citations(row_id, raw_path, pin, findings)

    entrypoint = pin.get(ENTRYPOINT_FIELD)
    if entrypoint is None:
        # A pin that names no entrypoint reaches neither of the two assertions
        # below, and canon obliges no pin to carry the field. Reported as
        # measured rather than passed over in silence, so a reader can tell an
        # inapplicable assertion from an unmade one.
        print(f"OK {row_id}: `{raw_path}` is registered and present; it names no "
              f"`{ENTRYPOINT_FIELD}:`, so the entrypoint assertions do not apply")
        return citations_ok

    # NOT coerced with `str()` before the containment helper runs: that would
    # turn `consumer_entrypoint: 17` into the string "17" and report it as a
    # merely-missing file, silently swallowing the helper's own non-string
    # refusal — the bench caught the coercion doing exactly that. The raw YAML
    # value is the claimed path, and it is a string only once the helper says so.
    entrypoint_path, refusal = resolve_in_tree(entrypoint)
    if refusal is not None:
        findings.append(
            f"FAIL {row_id}: the pin names `{ENTRYPOINT_FIELD}: {entrypoint!r}`, "
            f"which {refusal} — the published recipe invokes the entrypoint FROM "
            f"THE PINNED CHECKOUT, and a path outside it is unreachable there")
        # Terminal for this row: `consumption_rule` is compared against a PATH,
        # and there is no path to compare against. Reporting a second finding
        # that the rule "never names 17" would be noise, not an assertion.
        return False

    entrypoint = str(entrypoint)
    if not entrypoint_path.is_file():
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

    if ok and citations_ok:
        print(f"OK {row_id}: `{raw_path}` is present, its "
              f"`{ENTRYPOINT_FIELD}: {entrypoint}` resolves, and the row's "
              f"`{RULE_FIELD}` names that same path")
    return ok and citations_ok


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
