# Quickstart — seeing the third state work, and seeing it refuse

> **REWRITTEN FOR THE LANDED MODULE, 2026-09-02 (lane openxfactory-1d).** The
> version carried from PR #584 was written against THAT branch's reader —
> `read_spent_declarations`, `spent_refusal`, and a `SpentDeclaration` with
> `ruling`/`defect`/`count` — none of which exists in the implementation that
> actually landed (PR #587, squash `3fa222f3`), whose reader is
> `parse_spent_declarations` returning a LIST of declarations carrying
> `author`/`ruled_on`. **Every block below was run and its output pasted**;
> Copilot was right that the previous text could not run at all, and a
> quickstart that cannot run is worse than none because it looks like a
> reference.
>
> Two claims of the old text are also gone because they were PR #584's, not
> this branch's: the declaration is at changelog line **389**, not 374, and
> the family reads **green** here rather than carrying a declared red — the
> declaration is already live on `main`.

Run from a fresh clone of `opensoft/openxFactory` on this branch, never a
shared checkout. Python 3 with pytest; the checker is stdlib-only.

## 1. Read the declaration the way the family reads it

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
declarations = rtp.parse_spent_declarations(
    open("contracts/CHANGELOG.md", "rb").read())
v = {d.subject: d for d in declarations}["contract-v2.6"]
print("subject     ", v.subject)
print("entry       ", v.entry)
print("superseding ", v.superseding)
print("ruled by    ", v.author, v.ruled_on)
print("measurement ", v.measurement)
print("line        ", v.line)
print("missing     ", v.missing)
PY
```

Output:

```text
subject      contract-v2.6
entry        contract-v3.0
superseding  contract-v3.0
ruled by     Brett Heap 2026-09-02
measurement  PR #565 comment `5502452624`
line         389
missing      ()
```

**`entry contract-v3.0` is the line to read, and it is what this branch
hardens.** It says the declaration sits inside the changelog entry of the
bundle it names as superseding — the containment rule — and it is that answer
that ten measured escapes could each produce from somewhere the declaration was
not. Looked up BY SUBJECT rather than by position, so a second spent number one
day does not change what this reads.

## 2. Run the family over this repository

```bash
python3 scripts/doc-health.py --single-repo . | grep -A 3 "^### release-tag-publication"
```

Output:

```text
### release-tag-publication

- [info] …:contracts/releases/contract-v2.6.digests.yaml — contract-v2.6 is
  declared SPENT: it was cut, has no published annotated tag, and
  contract-v3.0 — itself cut, itself published and strictly later —
  superseded it. …
```

**One `info`, on the bundle's OWN release inventory**, which is the accepted
state. The family reads the changelog **at the published tip**, resolved with
`git ls-remote origin refs/heads/main` — so if your clone has not fetched that
tip you will get a SKIP naming the read instead, which is an environment fact
and not a corpus one:

```text
Skipped: …: contracts/manifest.yaml could not be read at the published tip
36aafb305 — the commit may not be present locally, which is not the same fact
as declaring no bundle
```

`git fetch origin` and run it again. **That skip is worth meeting once**: it is
the #338 conflation this family guards in both of its reads, and mistaking it
for a green is how PR #584 nearly banked one.

## 3. See it REFUSE — the guard, in one command

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
CUT = {"contract-v2.5", "contract-v2.6", "contract-v3.0"}
def why(line, entry="contract-v3.0", declared="contract-v3.0"):
    body = f"## {entry} — x\n\n{line}\n"
    d = rtp.parse_spent_declarations(body)[0]
    state = rtp._declaration_state(d, 1, CUT, declared)
    return None if state is None else state[1]
good = ("**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — "
        "CAUSE: never publishable — RULED BY Brett Heap, 2026-09-02 — "
        "MEASUREMENT: PR #565 comment 5502452624")
print("1 accepted      :", why(good))
print("2 no measurement:", why(good.split(" — MEASUREMENT")[0])[:66])
print("3 earlier succ. :", why(good.replace("`contract-v3.0`", "`contract-v2.5`"),
                               entry="contract-v2.5")[:66])
print("4 wrong entry   :", why(good, entry="contract-v2.6")[:66])
F = "`" * 3   # built, not typed, so this block's own fence survives
print("5 fenced example:", len(rtp.parse_spent_declarations(
    f"## contract-v3.0 — x\n\n{F}\n{good}\n{F}\n")))
print("6 opener alone  :", why("**SPENT BUNDLE:** trust me")[:66])
PY
```

Output:

```text
1 accepted      : None
2 no measurement: the declaration is missing the measurement of record
3 earlier succ. : contract-v2.5 is not STRICTLY LATER than contract-v2.6, and a tag
4 wrong entry   : the declaration names contract-v3.0 as the superseding bundle but
5 fenced example: 0
6 opener alone  : the line carries the reserved opener and no readable subject, so i
```

**`1 accepted: None` next to five refusals is the whole design in one screen**:
the state is entered by a record that exists and refused by every record that
does not. Row 5 is this branch's own — the identical line inside a **fenced
block** is not a declaration at all, so the form can be DOCUMENTED without being
PERFORMED, and neither an example nor a declaration hidden in a fence can spend
a bundle.

## 4. See a containment escape refused

The hardening in one comparison — the same well-formed declaration, moved out
from under its entry by a heading that is not a release heading:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
line = ("**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — "
        "CAUSE: c — RULED BY Brett Heap, 2026-09-02 — MEASUREMENT: PR #565")
for label, between in [("inside the entry", []),
                       ("under a `###` subsection", ["### disposition"]),
                       ("under `## Deprecations`", ["## Deprecations"]),
                       ("under a level-one heading", ["# Notes"]),
                       ("under an indented heading", ["  ## Notes"]),
                       ("under a Setext heading", ["Notes", "====="]),
                       ("under an empty heading", ["##"])]:
    doc = "\n".join(["## contract-v3.0 — a cut", ""] + between + ["", line])
    print(f"{label:28s} -> entry {rtp.parse_spent_declarations(doc)[0].entry}")
PY
```

Output — `contract-v3.0` is ACCEPTED, `None` is REFUSED, and only the first two
are inside the entry:

```text
inside the entry             -> entry contract-v3.0
under a `###` subsection     -> entry contract-v3.0
under `## Deprecations`      -> entry None
under a level-one heading    -> entry None
under an indented heading    -> entry None
under a Setext heading       -> entry None
under an empty heading       -> entry None
```

The `###` row is the load-bearing one in the other direction: this repository's
own declaration lives inside a `### \`contract-v2.6\` disposition` subsection of
the `contract-v3.0` entry, so a rule that closed on `###` would refuse the
declaration that makes `main` green.

## 5. See the reader REFUSE raw HTML

**Ruled 2026-09-03 (variant B): the reader parses no raw-HTML blocks — it
recognizes an opener and refuses to read past it.** Fences remain the only
opaque region. Same declaration in every document, only what sits above it
changes:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
F = "`" * 3   # built, not typed, so this block's own fence survives
line = ("**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — "
        "CAUSE: c — RULED BY Brett Heap, 2026-09-02 — MEASUREMENT: PR #565")
for label, above in [("no raw HTML", []),
                     ("a `<div>` above it", ["<div>"]),
                     ("a comment above it", ["<!-- x -->"]),
                     ("`<pre>` inside a fence", [F + "html", "<pre>", F]),
                     ("prose naming `<pre>`", ["the `<pre>` element"])]:
    doc = "\n".join(["## contract-v3.0 — a cut", ""] + above + ["", line])
    read = rtp.read_changelog(doc)
    stopped = "-" if read.raw_html is None else f"line {read.raw_html[0]}"
    entry = read.declarations[0].entry if read.declarations else "UNREAD"
    print(f"{label:24s} -> stopped {stopped:7s} entry {entry}")
live = rtp.read_changelog(open("contracts/CHANGELOG.md", "rb").read())
print(f"{'live changelog':24s} -> stopped", live.raw_html or "-")
PY
```

Output:

```text
no raw HTML              -> stopped -       entry contract-v3.0
a `<div>` above it       -> stopped line 3  entry UNREAD
a comment above it       -> stopped line 3  entry UNREAD
`<pre>` inside a fence   -> stopped -       entry contract-v3.0
prose naming `<pre>`     -> stopped -       entry contract-v3.0
live changelog           -> stopped -
```

**`UNREAD` is the point.** The declaration below the opener is well formed and
correctly contained — row 1 proves it would be accepted — and it is refused
anyway, because this reader has no model of what a renderer makes of the lines
below raw HTML and a construct it cannot parse must never be able to quiet a
finding. The changelog gets ONE `contested` `error` naming the line, and the
superseded-and-never-published `error` for the bundle stands beside it. Rows 4
and 5 are the controls in the other direction: an opener shown as an EXAMPLE
inside a fence is not an opener, and prose that merely mentions a tag is prose.
The last row is why the rule costs this estate nothing today — and it reds the
day that changes.

## 6. Run the tests

```bash
python3 -m pytest tests/doc-health/test_release_tag_publication.py -q
python3 -m pytest tests/doc-health -q
```

Expected on this branch: **120 passed** and **1485 passed**, zero failures in
both. There is no declared red here — `main` at `642ac147` reads **46** and
**1411**, also with zero failures, because the declaration landed with PR #587,
and 1411 − 46 + 120 = 1485. Anything failing is a real defect.
