# Design: govern-openspec-corpus-membership

Status: draft
Kind: design

Three decisions need recording, because each of them was reached against an
obvious cheaper alternative and the reasoning is not recoverable from the
diff.

## Decision 1 — a second path set, not a wider `GOVERNED_ROOTS`

**Chosen:** `LIFECYCLE_SCAN`, a set of explicit globs held beside
`GOVERNED_ROOTS` in `doc_health.corpus`, loaded into its own document list
and handed to four named families through one new `Context` field.

**Rejected:** appending `"openspec"` to `GOVERNED_ROOTS`.

The measurement is the whole argument, and it is sharper than "full
membership is expensive". Every expensive consequence traces to one variable.
`ctx.docs` is not merely the input to the check families — it is also the
input to the per-stage census, the governance and canon word totals, the
canon-share headline, the shared inventory and, through the inventory, the
document catalog. Growing it from 327 documents to 990 therefore does five
things at once, only one of which anybody wants:

- 121 of the 123 test failures are a single message,
  `duplicate inventory key: ('alpha', 'openspec/specs/widget/spec.md')`. The
  inventory already carries promoted specs as `artifact_type: promoted_spec`
  and would now receive the same files a second time as
  `governance_markdown`. That is not a test to update; it is a genuine
  two-paths-to-one-file collision in the corpus model, and widening the roots
  creates it in one line.
- The canon-share headline falls 13.2 points in this repository and 12.2
  points across the six-repo aggregation, purely because the denominator
  absorbs 814,507 words of proposal prose. Brett watches that number
  nightly. A metric that halves on the day the measurement changes has
  stopped reporting the corpus.
- `test_promoted_specs_join_without_expanding_the_governed_corpus` asserts,
  by name, that promoted specs join the inventory *without* expanding the
  governed corpus. The corpus model already holds an intention here and it
  is the opposite of the wider root.

Holding the lifecycle set separately buys the enforcement without any of
that. `ctx.docs` is byte-identical, so every consumer downstream of it is
byte-identical, and the four families that opt in are the only code that sees
a different world. The cost of the separate set is one field on `Context` and
four call sites — which is also, honestly, its risk: a fifth family added
later will read `ctx.docs` alone unless somebody remembers. §3 of tasks makes
that a test rather than a memory.

**RULED (2026-08-23, Brett, in-session multiple choice): this decision is adopted — a second path set, `GOVERNED_ROOTS` unchanged (OQ-1).** Worth
recording that the measurement did the work here rather than the argument:
Brett's first lean was the wider root, and the three bullets above are what
moved him. See proposal.md for the full ruling.

## Decision 2 — globs, not a directory

**Chosen:** `openspec/changes/**/proposal.md` and
`openspec/changes/**/review/*.md`.

**Rejected:** `openspec/`, and `openspec/changes/`.

Neither directory-shaped alternative changes what the lifecycle families
find. Measured: `ratified-provenance` fires 20 times over all of `openspec/`,
20 times over `openspec/changes/`, and 20 times over the glob set;
`succession-integrity` fires 4, 4 and 0. What the directory forms add is
`status-validity` noise — 536 fires over `openspec/`, 487 over
`openspec/changes/`, 48 over the globs — plus two false-positive classes the
globs exclude for free:

- `supporting-docs/source-snapshots/` holds BYTE-EXACT copies of staged files
  with a per-file sha256 manifest proving it. Their `Status: staged` is
  correct, and `location-conformance` already carries an explicit carve-out
  for it (`test_source_snapshots_keep_their_staged_status`, a 2026-08-15
  regression). A directory-shaped set re-breaks that carve-out through a
  different rule — "staged fragment outside `ideation/`" — which is how a
  fixed bug comes back wearing a different family's name.
- `archive/2026-07-09-concretize-prose-tagging-syntax` is the change that
  DEFINED the `xspec:` marker grammar. Its proposal and design necessarily
  carry deliberately malformed markers as examples, and `tag-hygiene` fires
  on both. The glob set still reaches its `proposal.md`, so that one fire
  survives — which is exactly why `tag-hygiene` is not one of the four
  families in Decision 3.

The glob form is also the honest one about what is being claimed. The claim
is not "OpenSpec is governance prose". It is "a proposal's lifecycle header
is a lifecycle header". A glob says that; a directory says something larger
that the measurement does not support.

**RULED (2026-08-23, Brett, in-session multiple choice): this decision is adopted, unopposed in prose — the two globs, declared as a pattern set (OQ-2).** The glob-not-directory boundary is the claim, so tasks §3.6
mutation-pins it structurally: flipping the set to bare `("openspec",)` must
fail §3.1, and the assertion is on the declared pattern set rather than only
on the resulting counts, because a count can pass for the wrong set.

**AMENDED ON THE FIX LAP (2026-08-23), in two ways that pull in opposite
directions and are both the ruling being applied rather than revised.** The
`review/*.md` half is WIDER than this decision's prose implied: Brett ruled
that every `review/` record under a packet is a governance document, not only
a ratification record, so the delta text widened to the glob rather than the
glob narrowing to the delta. Zero new findings followed — all eight of
openxFactory's non-ratification review records already carry
`Status: record`. Separately, membership is NARROWER by one explicit rule:
a path carrying a `supporting-docs`, `source-snapshots` or `evidence` segment
is excluded (`corpus.EVIDENCE_PARTS`), applied after the globs resolve. That
is the capability's own "byte-exact evidence" MUST NOT, which the first cut
disclosed as an open gap and left to a census. **The GLOBS themselves are
byte-identical to what was ruled**, which is the point of doing the exclusion
as a second, separately named rule rather than by editing the pattern: the
ruled artifact stays the ruled artifact, and the exclusion can be read,
tested and argued with on its own.

## Decision 3 — four families, chosen by measurement rather than by category

**Chosen:** `status-validity`, `standard-backing`, `ratified-provenance`,
`succession-integrity`.

The tempting shape is "all the lifecycle-conformance families", which would
also sweep in `location-conformance`, `record-immutability` and
`staged-candidate-aging`. Measured over the glob set, the first and third of
those contribute only false positives, and `record-immutability` contributes
nothing at all — its three fires under full membership are all `evidence/`
files, outside the set. So the category argument and the measurement disagree,
and the measurement wins.

`record-immutability` deserves its own sentence, because leaving it out is
the least obvious call here. Over the glob set it would fire zero times
today, so including it would be free. It stays out anyway: an archived
proposal is edited under the register's append discipline and Brett's
2026-08-10 ruling, not under the record-immutability family's
"revert the content edit" remedy, and wiring a family whose stated remedy
contradicts the governing discipline would put the two rules in a race the
first time an archived record is legitimately amended. That is a ruling to
take deliberately (OQ-6's neighbour), not a freebie to collect because the
count happens to be zero.

**RULED (2026-08-23, Brett, in-session multiple choice): this decision is adopted, unopposed in prose — the four families read the set (OQ-3).** The
`record-immutability` exclusion changed character on the same day and is
recorded here because the paragraph above now understates it. When it was
written, the race between the family's "revert the content edit" remedy and
the register's append discipline was hypothetical — zero fires, a hazard
argued from principle. OQ-6's ruling makes it certain: the campaign edits
**up to 56 archived records** (11 proposal respells + 44 proposal backfills
less whatever stops and reports + 1
archived review record), each an in-place overwrite named as an extension of
the 2026-08-10 append ruling — and every one of them is a document IN the
scan set, because the scan set is what the campaign is discharging. A family
whose remedy is "revert the content edit" would fire on the discharge
campaign itself. Left out on a zero count; kept out on a measured collision.

`standard-backing` fires zero times over the set and is included anyway,
because its absence would be the asymmetry: a proposal claiming
`Status: standard` without a promoted spec behind it is exactly the class of
claim this change exists to make checkable, and a family that costs nothing
today is the cheapest possible time to wire it.

## A note on the change id

The id says `corpus-membership` and the recommendation is that `openspec/`
does NOT join the corpus. That is deliberate. The parked question — task 5.1
of `sanction-ratified-record-spelling` — is a membership question, and the
record of how it was answered has to be findable from the question. A change
named for the answer would be findable only by someone who already knew it.
