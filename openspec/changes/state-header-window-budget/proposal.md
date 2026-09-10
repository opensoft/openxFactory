---
code_surface: none — MEASURED, not assumed: this packet's delta is pure requirement prose inside the ALREADY-PROMOTED `release-realization` requirement "Equivalent declaration sites for the ordered-delta parent declaration" — one paragraph added stating a rule `scripts/frontmatter_strict.py` already implements (`read_header_line`'s own docstring at lines 541-545, which already reads "FENCE LINES ARE SKIPPED BUT STILL COUNT toward the window", and its executable window arithmetic at lines 565 and 569, which counts the window from the document's own line 1 regardless of where a fence closes), and one scenario added asserting it; no existing sentence, bullet or scenario of the requirement is reworded, reordered or removed, so no `Removed from canon` marker is owed. `grep -rn "Equivalent declaration sites\|One parent declaration across both sites" scripts/ tests/` (checked 2026-09-10) returns exactly one hit, a docstring reference in `tests/sequenced_after/test_header_line.py`, and no test in this corpus pins this requirement's scenario count or scenario titles. Under `release-realization` a `code_surface: none` change archives on landing, exactly as `amend-neutral-product-pin-interim-copy-vocabulary` did for the same reason.
target_release: none — no code surface, no contract bundle, no digest set, no release tag, and nothing for any consumer to re-vendor: the rule this packet states in words is already what `scripts/frontmatter_strict.py` does in code, and already what codexFactory's vendored copy does, proved byte-equal to the source at `b91af6ea` in PR #906's own evidence (`evidence/realization-2026-09-10.md` § 3, re-run at that archive). The realization of a wording amendment is its promotion at archive, a separate act on Brett Heap's word, and not a build this packet owes.
sequenced_after: [accept-sequenced-after-header-line]
---

# Proposal: state-header-window-budget

Status: draft
Authored: 2026-09-10, lane codexfactory-1, on Brett Heap's resume ruling of
2026-09-10, verbatim **"fan out wide"** (authorization to author, not
ratification of this text) — carrying out lane codexfactory-1's own reply on
openxFactory PR
[#906](https://github.com/opensoft/openxFactory/pull/906#discussion_r3981322763),
which named this packet's shape.
**RATIFICATION IS OWED AND IS BRETT HEAP'S ACT** — see `.openspec.yaml`
`origin.approved_by` for the full disclaimer, and task 0.2 below.

## Origin

openxFactory PR #906 — the archive of `accept-sequenced-after-header-line`
(merged 2026-09-10T16:51:51Z at `92d0367c`) — carries a Copilot review comment
on `openspec/specs/release-realization/spec.md:440`
([discussion_r3981305715](https://github.com/opensoft/openxFactory/pull/906#discussion_r3981305715)),
quoted here in full because this packet exists to answer it and not to
paraphrase it:

> The requirement defines the header-line site as being within the first 15
> real lines and outside any leading `---` fence, but it doesn't explicitly
> state whether fence lines still count toward the 15-line window. The
> implementation (`scripts/frontmatter_strict.py:541-545`) treats fence lines
> as non-declaration lines that still count toward the window, so spelling
> that out here would reduce the risk of divergent consumer implementations.

Lane codexfactory-1 replied on that thread
([discussion_r3981322763](https://github.com/opensoft/openxFactory/pull/906#discussion_r3981322763)),
as itself and not as a ruling: the reading is correct, the packet's own
`tasks.md` § 2.3 already says so in words ("Fence lines still COUNT toward
the window — one window rule, the document's own"), and PR #906 was the
wrong place to fix it — editing the promoted requirement's text there would
have broken the sha256 byte-identity between the archived delta and the
promoted spec that pull request's own evidence rests on, and would have
amended ratified text with no ruling behind the amendment. The reply named
the remedy: a narrow `## MODIFIED` amendment, of the shape
`amend-marker-reason-boundary` and `amend-neutral-product-pin-interim-copy-vocabulary`
already took for comparably small gaps. **This packet is that amendment.**

## Why

**The requirement states one half of the rule and is silent on the other
half, and the two halves are easy to conflate.** The promoted requirement
"Equivalent declaration sites for the ordered-delta parent declaration"
says a header-line declaration sits "within the document's BOUNDED LIFECYCLE
HEADER WINDOW … and outside any leading `---` fence, whose lines are read by
the front-matter reader and MUST NOT be counted a second time as header
lines of the same document." That sentence answers ONE question — may a
fence's own lines be read AGAIN as a header-line declaration site? No — and
is silent on a DIFFERENT question it reads as adjacent: do a fence's lines
still occupy part of the window's fifteen-line BUDGET, or does the window
start counting fresh once the fence closes? A reader who has not read the
code could take either answer from that sentence, and a reader implementing
the rule from the prose alone — exactly codexFactory's position, since it
vendors the code but a FUTURE consumer might implement from the spec instead
— has nothing in the requirement text to settle it.

**The code has one answer, and it is not the more permissive one.**
`scripts/frontmatter_strict.py`'s `read_header_line` computes the window's
end as `min(window, len(lines))` against `lines`, the FULL list of the
document's real lines starting at index 0 = line 1 — the SAME index space
the fence occupies — while the scan's START moves past the fence
(`start = 0 if closing is None else closing + 1`, line 565; the scan itself
at `for index in range(start, min(window, len(lines))):`, line 569). The
window's upper bound never moves to account for the fence. Confirmed
empirically on this branch (not merely read): a `sequenced_after:` header
line sitting at the document's real line 19, behind a four-line fence, is
REFUSED as `NO_HEADER_LINE` — it would be ADMITTED under the reading "the
window is fifteen lines counted after the fence closes," which a fence
ending at line 4 would place at lines 5–19 inclusive — while a header line
at real line 15 behind the SAME fence IS read, because line 15 is the
window's own absolute edge, fence included. The docstring the Copilot
comment cites already states the same conclusion in words, at lines
541–545: "FENCE LINES ARE SKIPPED BUT STILL COUNT toward the window: the
window is the first `window` lines OF THE DOCUMENT … rather than a second
window measured from wherever a fence happens to end." Task 2.3 of the
archived packet's own `tasks.md` records the same design choice at
authoring time. Nothing here is a new reading; every source that speaks to
the question — the code, its docstring, the packet's own task record, and
Brett Heap's own PR #906 reply — agrees, and none of them is the promoted
requirement text itself.

**Silence in a promoted requirement is not neutral, because this requirement
exists so a consumer other than this repository can implement the rule from
prose.** The whole reason the header-line form exists is that codexFactory
writes its lifecycle headers unfenced and needed a reader; `accept-sequenced-after-header-line`
built that reader IN openxFactory and codexFactory VENDORS it byte-for-byte
rather than re-implementing it — so today no divergence is possible, the
vendored bytes being checked equal to the source at the pinned
`contract_ref`. But the requirement is written as the capability's statement
of the rule, independent of any one implementation, and a future consumer
implementing from the promoted spec instead of vendoring openxFactory's code
would have to guess the same thing a careful outside reviewer (Copilot) just
guessed wrong about. Stating the rule the code already enforces costs
nothing behaviourally and closes that gap for anyone who reads the
requirement rather than the implementation.

## What Changes

**ONE `## MODIFIED` requirement, and it is a pure addition.** The block below
targets "Equivalent declaration sites for the ordered-delta parent
declaration" — promoted in `openspec/specs/release-realization/spec.md` by
the archive of `accept-sequenced-after-header-line` (PR #906) — and adds:

- **One body paragraph**, inserted immediately after the paragraph defining
  the bounded lifecycle header window and before the paragraph on
  single-line values, stating that the window is counted from the
  document's own line 1, that a leading fence's lines (both `---`
  delimiters and every line between them) count toward that budget exactly
  as any other line does, and that the window is not re-measured as a fresh
  window starting after the fence closes.
- **One scenario**, `Fence lines consume the header window budget`, placed
  after the existing "The same bytes appear beyond the header window"
  scenario, asserting the concrete consequence: a header line a fence's
  length pushes past the window's last line is not read.

**Every existing sentence, bullet and scenario of the requirement is carried
verbatim.** Nothing is reworded, reordered, renamed or dropped, so this
delta owes no `Removed from canon by` marker and no `Merged into` marker —
those markers declare a deletion, and this change makes none. The other
promoted requirement of this capability's `accept-sequenced-after-header-line`
delta, "One parent declaration across both sites, and its retention," is
untouched and is not restated here.

**Sibling search, taken 2026-09-10 before authoring.** No other ACTIVE
change carries a `release-realization` spec delta at all
(`find openspec/changes -maxdepth 3 -path "*/specs/release-realization/*" -not -path "*/archive/*"`
returns nothing), and no open pull request on `opensoft/openxFactory` touches
`release-realization` or `frontmatter_strict` (checked via
`gh pr list --json number,title,files`). No active change collides with this
delta, so `modified-block-currency`'s two-writers ordering rule owes no
`Modified over` marker.

**The ledger's own `class` field reads `co-modifier`, not `sole`, and that
is correct rather than a defect.** This change's `## MODIFIED` block writes
the same requirement key — `release-realization` / "Equivalent declaration
sites for the ordered-delta parent declaration" — that
`accept-sequenced-after-header-line`'s own `## ADDED Requirements` block
wrote, and the per-change sweep ledger counts that ARCHIVED adder as the
partner regardless of the active-collision question above, which is
narrower and answered separately. Seeding this change's row
(`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
'#921'`) flips `accept-sequenced-after-header-line`'s own row from `sole` to
`co-modifier` in the same re-seed — the ledger's own documented "partner
flip" mechanic, not a hand edit.

## Impact

- **Affected spec:** `release-realization` — ONE `## MODIFIED` requirement,
  one body paragraph added, one scenario added (now five), nothing removed.
- **Affected code:** none. `scripts/frontmatter_strict.py` already implements
  the stated rule; this packet changes no script, test, workflow or
  contract.
- **Affected consumers:** none. codexFactory's vendored copy already carries
  the behaviour this packet states in words; no re-vendor, no pin advance,
  no re-pin ceremony is owed by this change.
- **Backward-compat:** total. No document in this corpus, or in codexFactory's,
  reads differently before and after this change; only the promoted
  requirement's own words move.

## Open questions

None. The fact this packet states is settled by the code, by the archived
packet's own task record, and by Brett Heap's own reply on PR #906; the only
thing owed is the wording ratification itself (task 0.2).
