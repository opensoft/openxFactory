# Ratification — 2026-09-09

Status: record

## Decision

RATIFIED by Brett Heap.

## Authority, and that it is first-hand

Brett Heap's instruction, verbatim: **"ratify 813"** — given
**2026-09-09T03:19Z**, in his own message, **first-hand** to lane
`codexfactory-1` (session name `codeXfactory-1`,
https://claude.ai/code/session_01SaMMgNoPTARduWJ4956UBg), which writes this
record.

**NO RELAY.** The word was heard in the session that acts on it, by the lane
that authored the packet. There is no second-hand path to disclose, which is the
condition `add-openspec-cli-pin`'s own ratification record had to state and
could not — its authoring lane correctly refused a second-hand word before the
first-hand one arrived. This is that shape satisfied rather than worked around.

## The earlier ruling, and why it was not this one

**Brett Heap, 2026-09-08T14:14:49Z, first-hand, in session**, verbatim
*"Vendor a lockfile (Recommended)"*, on a four-option packet whose other three
exits — enumerate the resolved tree in the pin, vendor the built tree as one
artifact by digest, accept the shortfall as declared — are recorded with their
reasons in `design.md` § 1.

That ruling **authorized the AUTHORING and named no view on the content.** The
packet has said so in three places since it was written (`proposal.md` header,
`tasks.md` header, `design.md` § 0), and task 5.1 was left unticked to hold the
gap open. This record closes it. Two words, one operator, two days, two
different decisions — the first chose the exit, the second accepts the text —
and both are recorded because both happened.

## The text ratified

The packet at head **`f2f7ee8d`** (openxFactory PR
[#813](https://github.com/opensoft/openxFactory/pull/813)), **plus the cosmetic
edits in this commit, named rather than implied**:

1. `design.md` § 0 and `evidence/dependency-closure-2026-09-08.md` § header —
   where the prose called `codeXfactory-1` a *lane*, it now reads
   "lane `codexfactory-1` (session name `codeXfactory-1`)", per lane-collision
   protocol Amendment 2: the machine key is lowercase and the display/session
   name keeps the capital. Raised as Copilot threads 12 and 13 on 2026-09-09 and
   folded in here rather than deferred, because a provenance record that
   mis-names its own author is the one kind of cosmetic defect a ratification
   record cannot carry.
2. `proposal.md` — `Status: draft` → `Status: ratified`, front matter and body,
   with the `Ratified:` line this record backs.
3. `tasks.md` — task 5.1 ticked, citing this file. `Status: draft` →
   `Status: ratified`, and the header paragraph that said ratification had not
   happened rewritten to say when it did.

Nothing else moves in the ratifying commit. No contract byte, no lockfile byte,
no pin field, no verifier line, no test.

## What ratification changes, and what it does not

**CHANGES:** the `Status:` header of `proposal.md`, `tasks.md` and `design.md`;
the `Ratified:` / `Ratified by:` citation each of those carries; the tick on task
5.1; and the packet's eligibility to be archived once tasks 5.2 and 5.3 are met
at the gate. (`design.md`'s header, and the two paragraphs that still said a
citation was owed, were completed in the FOLLOW-UP commit named in the pull
request rather than the ratifying one — Copilot caught the packet asserting two
different states about itself. `evidence/` and this record carry
`Status: record`, which is their correct lifecycle value and not a draft; the
spec delta carries no `Status:` header, as no spec delta in this repository
does.)

**DOES NOT CHANGE:** anything normative. The two ADDED requirements in
`neutral-product-pin` are ratified **as written** and not re-opened; no
requirement text, scenario, contract, workflow, digest or pin value moves by
this act. Tasks 5.2 (validation re-run at the archive gate) and 5.3
(realization evidence) remain **unticked and owed** — ratification is not an
archive, and the gate is re-run at archive time rather than trusted from here.
Group 6 is successor work and is untouched.

## What this ratification covers, as reviewed

The packet as it stands after **four Copilot review rounds** across
2026-09-08/09 — **13 threads, 11 taken and 2 cosmetic folded in here**, every
one replied to in-thread and resolved. Recorded in full in
`evidence/dependency-closure-2026-09-08.md` § 11. In substance the ratified
content is: the vendored `contracts/openspec-cli-pin.1.12.0.package-lock.json`
(80 packages, every one resolved and addressed); the pin's three new fields; the
verifier bound to them across all five refusal arms; `npm ci --ignore-scripts`
through a manifest DERIVED from the lockfile's own root entry; the reuse cache
keyed on both addresses; and all three callers of `resolve_pinned` bound to the
closure.

## The design decisions ratified AS WRITTEN

Named individually, because each was a live choice and a ratification that left
them implicit would be a ratification of nothing in particular:

- **The `1.2.0` rollback entry is UNCOVERED**, declared as such in the pin
  itself. A rollback is a change to author, not a revert to apply. A
  speculatively generated lockfile for an old referent would record what today's
  ranges resolve to, which is a fiction of reproducibility rather than a record
  of one (`design.md` § 6.3).
- **`pin-lockfile-mismatch` is the SINGLE new refusal code**, carrying five arms
  (digest drift, referent disagreement, size drift, an unaddressed entry, a root
  that declares nothing to install). It is not an overload of
  `pin-integrity-mismatch`: the two send a reader to different files
  (`design.md` § 2.3).
- **The cache-hit boundary stands as built:** `assert_installed_package` runs at
  INSTALL, not on a cache hit, consistent with the existing "only the install is
  reused" split, with `assert_reported_version` still running on every path.
  Named here so it is a ratified boundary rather than an unexamined one.
- **The two pre-existing host-absolute paths in
  `tests/openspec_cli_pin/fixtures/*.json` are LEFT STANDING** — captured CLI
  output landed on `main` by `bump-openspec-cli-pin-to-1.12` (`baae60fd`),
  untouched by this pull request and not this packet's to redact.

## Limits

This record ratifies **one packet's text**. It does not archive it, does not
move any consuming repository's wiring, does not bump the pin, does not repoint
`pytest-suite.yml`, and does not close the trust-on-first-use of the 79 registry
integrity values captured when the lockfile was generated — which
`design.md` § 6.1 declares open and this ratification does not silently close.
