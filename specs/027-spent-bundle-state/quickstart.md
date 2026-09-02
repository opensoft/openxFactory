# Quickstart — seeing the third state work, and seeing it refuse

Run from a fresh clone of `opensoft/openxFactory` on this branch, never a
shared checkout. Python 3 with pytest; the checker is stdlib-only.

## 1. Read the declaration the way the family reads it

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
d = rtp.read_spent_declarations(open("contracts/CHANGELOG.md", "rb").read())
v = d["contract-v2.6"]
print("subject     ", v.subject)
print("entry       ", v.entry)
print("superseding ", v.superseding)
print("ruling      ", v.ruling)
print("measurement ", v.measurement)
print("missing     ", v.missing, "defect", v.defect, "count", v.count)
print("refusal     ", rtp.spent_refusal(v, "contract-v2.6",
                                        {"contract-v2.6", "contract-v3.0"}))
PY
```

Expected — and `refusal: None` is the point, because it means every check a
changelog read can perform has passed:

```text
subject      contract-v2.6
entry        contract-v3.0
superseding  contract-v3.0
ruling       Brett Heap, 2026-09-02
measurement  PR #565 comment `5502452624`
missing      () defect None count 1
refusal      None
```

## 2. Run the family — and understand what you will see BEFORE the merge

```bash
python3 scripts/doc-health.py --single-repo . | grep -A 3 "^### release-tag-publication"
```

**BEFORE this branch is merged** you will see the `error`, and that is correct:

```text
- [error] …:contracts/manifest.yaml — contract-v2.6 was cut and SUPERSEDED
  without ever being published: …
```

The family reads the changelog **at the published tip**, resolved with
`git ls-remote origin refs/heads/main` — so it reads `main`'s changelog, not
your working tree's. **AFTER the merge** the same command answers:

```text
- [info] …:contracts/releases/contract-v2.6.digests.yaml — contract-v2.6 is
  SPENT: it was cut, was never publishable, and is declared spent by the
  reserved SPENT declaration at contracts/CHANGELOG.md line 374, inside the
  contract-v3.0 entry — …
```

To see that now, without waiting: see
[`evidence/post-merge-proof.md`](./evidence/post-merge-proof.md), which pushes
this branch to a bare repository as its `main` and runs the family against it.

## 3. See it REFUSE — the guard, in one command

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import release_tag_publication as rtp
CUT = {"contract-v2.5", "contract-v2.6", "contract-v3.0"}
def read(line, entry="contract-v3.0"):
    body = f"## {entry} — x\n\n{line}\n"
    return rtp.read_spent_declarations(body.encode())
def why(line, entry="contract-v3.0", subject="contract-v2.6"):
    d = read(line, entry).get(subject) or read(line, entry)[None]
    return rtp.spent_refusal(d, subject, CUT) if d.subject else d.defect

good = ("**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — "
        "CAUSE: never publishable — RULED BY Brett Heap, 2026-09-02 — "
        "MEASUREMENT: PR #565 comment 5502452624")
print("1 accepted      :", why(good))
print("2 no measurement:", why(good.split(" — MEASUREMENT")[0])[:70])
print("3 earlier succ. :", why(good.replace("`contract-v3.0`",
                                            "`contract-v2.5`"),
                               entry="contract-v2.5")[:70])
print("4 wrong entry   :", why(good, entry="contract-v2.6")[:70])
print("5 declares self :", why(good.replace("SUPERSEDED BY `contract-v3.0`",
                                            "SUPERSEDED BY `contract-v2.6`"),
                               entry="contract-v2.6")[:70])
print("6 opener alone  :", why("**SPENT BUNDLE:** trust me")[:70])
PY
```

Expected:

```text
1 accepted      : None
2 no measurement: the SPENT declaration naming contract-v2.6 at contracts/CHANGELOG.md l
3 earlier succ. : the SPENT declaration naming contract-v2.6 names contract-v2.5 as its
4 wrong entry   : the SPENT declaration naming contract-v2.6 sits in the contract-v2.6 e
5 declares self : the SPENT declaration naming contract-v2.6 names contract-v2.6 as its
6 opener alone  : the reserved opener is used but no backtick-quoted bundle name follows
```

**`1 accepted: None` next to five refusals is the whole design in one screen**:
the state is entered by a record that exists and refused by every record that
does not.

## 4. Run the tests

```bash
python3 -m pytest tests/doc-health/test_release_tag_publication.py -q
```

Expected on this branch: **50 passed, 1 failed** — the failure being
`test_this_repository_reads_zero_and_the_probe_can_fire`, which reads the live
remote `main`. It goes green at the squash and is not edited. Anything else
failing is a real defect.

```bash
python3 -m pytest tests/doc-health -q          # 1412 passed, 1 failed (same one)
```
