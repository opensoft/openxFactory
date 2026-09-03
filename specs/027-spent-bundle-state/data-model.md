# Data model — the third state, Phase 1

Everything below lives in `scripts/doc_health/release_tag_publication.py`.
Nothing here is a new report type: the state's findings are instances of the
package's shared `Finding`, and the module gains no severity constant — it
reuses `INFO`, `WARNING` and `ERROR` as the ruling assigns them.

## 1. The reserved form

```text
**SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>
```

| Part | Constant / pattern | Rule |
|---|---|---|
| opener | `SPENT_OPENER = "**SPENT BUNDLE:**"` | RESERVED. No other line in `contracts/CHANGELOG.md` may BEGIN with it. Matched at column 0 with `str.startswith` — a list item or an indented line does not "begin a line with it", which keeps the rule predictable. |
| subject | `_SPENT_SUBJECT` | Backtick-quoted, immediately after the opener. Unreadable → `defect`, keyed under `None`. |
| separator | `_SPENT_SEP = re.compile(r"\s+—\s+")` | RESERVED WITHIN the line. A segment sitting where no element is defined → `defect`. |
| containing entry | `_ENTRY_HEADING = re.compile(r"^##\s+(contract-v\d+\.\d+)\b")` | The most recent such heading ABOVE the line. None where the line precedes every entry. |
| ruling | `_RULED_BY` | `<author>, <YYYY-MM-DD>`. A missing date is reported as the `ruling date` specifically, not as the whole ruling. |
| elements | `_SPENT_ELEMENTS` | `[(prefix, reported name)]`, in the form's own order: `SUPERSEDED BY`/superseding bundle, `CAUSE:`/cause, `RULED BY`/ruling, `MEASUREMENT:`/measurement of record. The KEY is the literal prefix; the VALUE is the name a finding uses, because *which* element is missing is what the scenario asks the finding to say. |

**The backticks are the FORM's, not the NAME's.** Both bundle names are
unwrapped before comparison; a superseding name written WITHOUT backticks is
taken as written rather than refused, because it resolves to the same bundle and
refusing a correct disposition on its punctuation would report a defect that is
not there.

## 2. `SpentDeclaration` — one line as READ, never as judged

| Field | Type | Meaning |
|---|---|---|
| `subject` | `str \| None` | The bundle declared spent. `None` where the line names none. |
| `entry` | `str \| None` | The `## contract-vX.Y` entry containing the line. |
| `superseding` | `str \| None` | Unwrapped. |
| `cause` | `str \| None` | Read for PRESENCE, never for truth. |
| `author`, `date` | `str \| None` | The ruling, split. |
| `measurement` | `str \| None` | Read for PRESENCE, never for truth. |
| `lineno` | `int` | Named in every finding, so a reader can go to the record. |
| `missing` | `tuple[str, ...]` | Element names absent or EMPTY. Order-preserving and de-duplicated. |
| `defect` | `str \| None` | A non-element malformedness: an unreadable subject, or a separator inside an element. |
| `count` | `int` | How many declarations named this subject. `> 1` is a refusal all by itself. |
| `ruling` (property) | `str \| None` | `"<author>, <date>"`, or None where either half is missing. |

**Why `count` and not a collapse.** Two records of one disposition is how they
come to disagree, so the reader COUNTS rather than de-duplicating and the
ladder refuses ALL of them. A reader that kept only the last would silently
prefer one story.

## 3. The four new action constants, beside the module's existing four

| Name | Used by | Why its own name |
|---|---|---|
| `_SPENT_ACTION` | the ACCEPTED `info` | Says no action is owed, says the obligation was EXTINGUISHED rather than MET, and names the one way the state can be made to disappear so that a reader knows not to take it. |
| `_SPENT_PROVISIONAL_ACTION` | the PROVISIONAL `warning` | Names publishing the SUPERSEDING bundle's tag — the act that resolves the state — and says the obligation has MOVED rather than been discharged. |
| `_SPENT_REFUSED_ACTION` | every refusal, and the declared-bundle refusal | Says repair-or-withdraw, and says why the superseded finding stands beside it. |
| `_SPENT_ORPHAN_ACTION` | the orphan-subject `warning` and the no-subject `error` | Says correct the SUBJECT, and says the real bundle is still reported — which is the fail-closed sentence a typo must not defeat. |

Four names rather than reuses, for the reason the module already applies to its
severity constants: each answers a different act, and a shared constant would
move all four when one was rewritten.

## 4. The path rule — the state's identity

```python
def inventory_path(bundle: str) -> str:
    return f"{RELEASES}/{bundle}.digests.yaml"
```

| Finding | Severity | Path | Class |
|---|---|---|---|
| ACCEPTED | `info` | `contracts/releases/<subject>.digests.yaml` | `contested` |
| PROVISIONAL | `warning` | same | `auto-fixable` |
| REFUSED (any of six reasons) | `error` | same | `auto-fixable` |
| names the currently declared bundle | `error` | `contracts/releases/<declared>.digests.yaml` | `auto-fixable` |
| SUBJECT never cut | `warning` | `contracts/CHANGELOG.md` | `auto-fixable` |
| no readable SUBJECT | `error` | `contracts/CHANGELOG.md` | `auto-fixable` |

**Only the ACCEPTED `info` is `contested`, and that asymmetry is deliberate.**
A contested finding that VANISHES raises an `uncited-resolution` ERROR. The
spent state is PERMANENT, so its disappearance is exactly what must be
re-raised. A REFUSAL, by contrast, is meant to disappear — the declaration gets
repaired — and classing it `contested` would turn every correct repair into an
uncited-resolution error, which is the trap `release-inventory-drift`'s own
tests record for a cut-resolved finding.

`_finding` gained a `path=MANIFEST` DEFAULT rather than a new helper, so every
finding predating this state keeps the identity it had, byte for byte.

## 5. The three outcomes as a control flow

```text
absent tag                      (after ok / lightweight / misplaced have continued)
├── bundle == declared
│   ├── a declaration names it   → error (refused) …then fall through
│   └── distance grading         → unchanged
└── bundle != declared
    ├── no declaration           → superseded error            (UNCHANGED)
    ├── spent_refusal(...) != None → refused error + superseded error
    └── successor's tag state
        ├── unlistable           → Skip naming the successor
        ├── ok                   → ACCEPTED info (contested)
        └── otherwise            → PROVISIONAL warning  (superseded SUPPRESSED)

after the loop
├── declaration keyed None       → error on the changelog
└── subject ∉ (cut | {declared}) → warning on the changelog
```

`spent_refusal` checks, in order: `count > 1`; `defect`; `missing`; superseding
== subject (a bundle cannot declare itself spent); `entry != superseding`
(containment); superseding ∉ cut; superseding's version unshaped or not
STRICTLY GREATER (OD-9).
