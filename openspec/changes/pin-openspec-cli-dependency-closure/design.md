# Design: pin-openspec-cli-dependency-closure

Status: draft

## 0. The ruling, recorded verbatim, and what it did and did not settle

**Brett Heap, 2026-09-08T14:14:49Z, first-hand, in session**, on a four-option
packet put to him by lane `codeXfactory-1`. The timestamp is the one the lane's
CLAIMED comment carries on openxFactory PR #667.

The four options, as they were put:

1. **Vendor a lockfile (Recommended)** — *an authored lockfile committed beside
   the pin, its digest recorded in the pin, the installer and verifier bound to
   it; standard npm mechanism, regenerated per bump.*
2. **Enumerate the resolved tree in the pin contract** — record every resolved
   package and its integrity as pin fields, and have the verifier install
   against that enumeration.
3. **Vendor the built tree as one artifact by digest** — build `node_modules`
   once, archive it, record ONE digest over the archive, and unpack that.
4. **Accept the shortfall as declared** — change nothing; the pin's header
   already states that the closure is open, and a declared gap is not a hidden
   one.

**He chose (1), verbatim: "Vendor a lockfile (Recommended)".**

**THE RULING AUTHORIZED THE AUTHORING AND NOT THE CONTENT.** It settles which of
four exits is taken and nothing further: not the path, not the field names, not
the refusal code, not the rollback question, not one line of what follows. Every
judgment below is this lane's, is listed as such, and is open to a reviewer.
This packet carries `Status: draft` and owes a ratification citation from a
separate act.

## 1. Why the other three were not chosen

**Recorded because the house records them, and because the reasons are the
argument for the shape of what was built.**

### Option 2 — enumerate the resolved tree in the pin contract

**It re-implements a lockfile in a grammar no installer reads.** The 80 packages
would become 80 entries in `contracts/openspec-cli-pin.yaml`, each needing a
name, a version, a resolved URL and an integrity — and then the verifier would
have to *turn that enumeration back into something npm can install*, because npm
does not consume a YAML sequence. The only honest way to do that is to write a
`package-lock.json` from it at run time, which is option 1 with a lossy
intermediate representation and a hand-written serializer between the pin and
the tool.

It also breaks a property this pin file depends on. `read_pin` is a deliberately
NARROW reader — "this reader parses only the pin's own grammar and does not
understand …" — and the pin's own header argues at length for why it stays
narrow. Eighty nested entries with four keys each would either force a general
YAML parser into the one file whose whole design is a refusal to have one, or
force 320 lines of hand-maintained sequence into a file a human is expected to
review on every disposition change. And the file is a REGISTERED contract row
that five repositories read; growing it by an order of magnitude for data npm
already knows how to write is a cost paid by every reader of it, forever.

### Option 3 — vendor the built tree as one artifact by digest

**It makes openxFactory the redistributor of 80 packages it does not own.** The
strongest technical form of the closure — one digest over the exact bytes that
run — is also the form that puts ~14 MB of third-party JavaScript into this
repository, under 80 separate licences, with openxFactory as the party
distributing it. `neutral-product-pin`'s whole direction is that openxFactory
CONSUMES an external neutral product and does not own it; `contracts/README.md`
says of this very pin, in its own words, that openxFactory "does NOT own, vendor
or publish `@fission-ai/openspec`". Vendoring its transitive tree is exactly the
vendoring that sentence refuses.

It is also brittle in a way a lockfile is not: a built tree is
platform-shaped (optional dependencies, binary artifacts, symlink layout), so
one archive is one platform's answer, and a second platform would need a second
archive and a second digest. And it would make every bump a 14 MB diff nobody
can review, which converts a governed act into a rubber stamp.

### Option 4 — accept the shortfall as declared

**It was the standing position, and this change exists because that position
expired.** It was defensible while the pin was one repository's experiment: the
gap was declared in the pin's header rather than hidden, `--ignore-scripts` took
the sharpest edge off it, and #667 named the repair as successor work in
writing. What changed is the load. Five repositories now gate on this entrypoint
(codexFactory, MedxFactory, LedgerxFactory, AdxFactory and openxFactory), and
since 2026-09-08 `openspec-cli-pin` is a REQUIRED status check on openxFactory's
`main` — verified against the live ruleset, org ruleset **22551797**, named
*"openxFactory pin-gate (require openspec-cli-pin)"*, listed among `main`'s
required contexts beside `pytest-suite` and `lane-line`. A declared gap in a
required check is a declared gap in the thing that stops merges. Option 4 also
answers none of the question it was offered against: it leaves five gates
resolving nine caret ranges independently, and it leaves the pin's central claim
— that WHICH TOOL ADJUDICATED is a fact — true of one file and false of the
79 it runs on.

## 2. What was built, and the one decision inside each piece

### 2.1 The lockfile: path, name, and how it resolves

**`contracts/openspec-cli-pin.1.12.0.package-lock.json`, recorded in the pin as
the BARE NAME `openspec-cli-pin.1.12.0.package-lock.json`.**

*Under `contracts/`* because it is part of the pin, and the pin is the contract;
a lockfile in `scripts/` or at the root would be a governance artifact filed
under an implementation detail.

*Named for the pin AND for the version* — `openspec-cli-pin` + `1.12.0` —
because a bump then ADDS a file rather than silently rewriting the one the
previous referent was installed through. A reader looking at a tree with two
lockfiles in it can see at a glance which version each belongs to, and a
`git log` over the new file is that version's whole closure history. (The
alternative, one `openspec-cli-pin.package-lock.json` rewritten in place, buys a
smaller directory and pays for it by making "which tree did the 1.12.0 pin
install?" a question about a diff.)

*Recorded as a BARE NAME and not as a repository-relative path*, resolving
`pin_path.parent / name` and nowhere else. Three things follow, and all three
were wanted: a lockfile cannot wander into another directory, no path traversal
is admitted so none has to be sanitized, and the rule survives `--pin PATH` —
a synthetic pin in a temporary directory and the real pin in `contracts/` each
find their OWN lockfile and neither can reach the other's, which is what makes
the test suite's fixtures honest.

### 2.2 The pin's three new fields

`lockfile:`, `lockfile_integrity:`, `lockfile_packages:` — flat scalars beside
`tarball:`, in the shape `integrity:`/`shasum:` already established, rather than
a nested `dependency_closure:` mapping. There is exactly ONE current referent, so
a sequence would be a container holding one thing; the rollback's answer lives in
the rollback block where the rest of the rollback's answers already live.

`lockfile_packages:` is corroboration and is CHECKED, on the pin's own stated
rule about `shasum:`: *"a pin that records a value nothing verifies invites the
value to drift into being wrong without anyone noticing."* It is recorded because
a reviewer reads a count and not a digest.

### 2.3 The refusal code: ONE new one, and where it does NOT apply

`pin-lockfile-mismatch` is added to `REFUSAL_CODES` — the vocabulary is
enumerated and asserted by a test, so it is extended rather than overloaded.

**It is not a synonym for `pin-integrity-mismatch`**, and the difference is which
file a reader is sent to. `pin-integrity-mismatch` says *the REGISTRY served
bytes this repository does not pin* — remedy: re-cut the pin, or distrust the
registry. `pin-lockfile-mismatch` says *the two halves of THIS REPOSITORY'S OWN
pin disagree with each other* — remedy: regenerate the committed lockfile at the
pinned version. Collapsing them would name the wrong defect in the one message a
reviewer reads.

**One code covers three disagreements**, in the order of how much each says, and
that grouping copies `verify_artifact`'s own precedent of reporting INTEGRITY
DRIFT ahead of SHASUM DRIFT under one code: `LOCKFILE DIGEST DRIFT` (the bytes
are not the bytes the pin addresses — everything else would be a statement about
a file this pin does not name), `LOCKFILE REFERENT DISAGREEMENT` (the lockfile
locks a different `@fission-ai/openspec`, or none), `LOCKFILE SIZE DRIFT` (the
tree is not the recorded size).

**Two codes it deliberately is NOT.** A pin that declares NO lockfile is
`pin-tag-only`, because unresolved caret ranges ARE a moving reference and *"the
moment a pin trusts a range the fail-closed property is gone"* is that code's own
sentence — quoted from `neutral-product-pin`, and as true of a dependency range
as of a version range. A lockfile that is absent, is not JSON, or carries no
`packages` object is `pin-unreadable`, on the division that file already draws: a
MISMATCH is a disagreement between two well-formed statements a reviewer can act
on, and an unreadable lockfile is the state in which no such comparison can be
reached at all — the same state an absent pin file is in, and it takes the same
code.

### 2.4 `npm ci`, and the derived staging manifest

**`npm ci` and not `npm install`.** `npm install` treats a lockfile as a starting
point and may RE-RESOLVE a range that has since acquired a newer satisfying
version; `npm ci` treats it as the answer, installs exactly what it records,
verifies every package against the integrity recorded there, and refuses outright
when the manifest and the lockfile disagree. Only the second makes *"the
installed tree IS the pinned tree"* a fact about the run rather than a hope about
npm's behaviour. A test asserts the argv that actually ran carries `ci` and that
no `install` runs at all.

**The staging `package.json` is DERIVED from the lockfile, not committed beside
it.** `npm ci` needs both files and refuses when they disagree — so a second
COMMITTED file would be a second copy of the dependency declaration, which is the
exact defect this whole pin family exists to end, and the two would eventually
move apart the way `pytest-suite.yml`'s literal moved apart from the pin.
Deriving the manifest from the lockfile's own root (`""`) entry makes them agree
BY CONSTRUCTION: there is one written declaration and the other is a function of
it.

**`--ignore-scripts` stays, and its justification narrows rather than
disappears.** It was a MITIGATION of an open shortfall — an *unpinned* transitive
dependency must not run a lifecycle script inside a gate. The tree is no longer
unpinned, so the flag is now defence in depth over a KNOWN tree; a pinned
dependency carrying a hostile install script is still a dependency carrying one,
and a gate is not the place to run it.

**The executable moved from `<prefix>/bin/openspec` to
`<prefix>/node_modules/.bin/openspec`**, because a lockfile installs a PROJECT
and not a global. The property that matters is unchanged and is still asserted:
the executable is a PATH this code returns, never a name a shell resolves, so
`--path-mode` remains the only mode that can be affected by what is installed on
a machine.

### 2.5 The cache key

`cache_key()` folds `sha512(lockfile_bytes)[:16]` into the reuse directory's name
beside the package, the version and the shasum, and the `.pin-verified` stamp now
carries BOTH addresses.

**A different tree is a different install.** Before this change two runs at one
artifact could legitimately produce two different `node_modules`, and the cache
had no way to tell them apart: one directory served both, and whichever ran first
decided what the second one got. That was invisible and it was the shortfall's
sharpest practical edge. Now a lockfile edit lands in a NEW directory, and the
old one is neither reused nor silently overwritten.

The 16 hex characters are a DIRECTORY NAME and not a referent — the referent is
re-checked by `verify_lockfile` over the real bytes on every run, exactly as the
artifact's is, so no run inherits a previous run's verdict about either file.

### 2.6 `--tarball`, narrowed honestly

`--tarball` still verifies the supplied bytes against the referent, and the
INSTALL now goes through the lockfile like every other path. That is not a
weakening: `verify_lockfile` has already refused unless the lockfile's entry for
the package carries THIS integrity, so the CLI bytes `npm ci` installs are the
bytes just verified. What the mode saves is the `npm pack` — which is what it
always saved, because the nine caret-ranged dependencies were never inside that
tarball and were always fetched. The remediation trailer is amended to say so
rather than left implying an offline mode that never existed.

## 3. What did NOT move, deliberately

- **`.github/workflows/openspec-cli-pin-gate.yml` and
  `.github/workflows/pytest-suite.yml`: byte-unchanged.** This is the
  single-source property paying out. Neither ever named the version, so neither
  has to learn the lockfile: the invocation each already runs installs the
  closure because the verifier reads the pin. The two tests that assert those
  workflows carry no copy of the pin are TIGHTENED here — they now also refuse
  the lockfile's name and its address — rather than relaxed.
- **The four `dispositions:` entries and the disposition machinery: untouched.**
  This packet adds none, retires none and reads none. The
  `(repo, item, path)` triple test therefore does NOT move, and that is a
  deliberate statement rather than an oversight: a change to this pin that grew
  the exception list would be a change nobody read, which is what that assertion
  is for.
- **`version`, `integrity`, `shasum`, `tarball`: byte-unchanged.** The referent
  does not move in this change. A closure change and a version change are two
  human-only acts and they are not ridden together.
- **No consuming repository is edited.** Each already invokes this entrypoint
  from a pinned openxFactory checkout, so each gains the closure at its next
  `contract_ref` advance, and each begins installing an 80-package pinned tree
  instead of resolving nine ranges without noticing.
- **`contracts/manifest.yaml` gains no row.** The lockfile is a MEMBER of the
  pin, addressed by the pin, and not a second published claim. Registering it
  separately would invite a consumer to read it without the pin that gives it
  meaning.

## 4. Why the spec delta ADDS and does not MODIFY

**Two ADDED requirements in `neutral-product-pin`, and nothing MODIFIED.**

The tempting MODIFY is *"An external neutral product is pinned by commit and
digest, never by tag"* — the requirement `add-openspec-cli-pin` already extends
to admit a published-artifact referent. It is not taken, for two reasons.

**It would make this packet a co-modifier of a requirement two ACTIVE changes
already contest.** `add-openspec-cli-pin` carries a `## MODIFIED` block on that
requirement today and has not archived; a MODIFIED requirement replaces the
WHOLE block, so two unarchived changes modifying it would leave whichever
archived second silently overwriting the first's text. The estate has a name for
the class of defect that produces — it is what the pinned CLI's own
scenario-currency check exists to catch, and what all four of this pin's
dispositions are about.

**And the obligation is genuinely NEW, not a refinement of an old one.** That
requirement governs WHAT A PIN'S REFERENT IS. This change governs something the
capability has never spoken about: that where a pinned artifact RESOLVES
dependencies at install time, the resolution itself is pinned, and the install
runs through the pinned resolution. Writing it as an amendment to the referent
rule would bury a new duty inside a sentence about digests.

The two are split rather than merged because they have different owners and fail
in different places. The first is about the FILE and the RUN — declared,
addressed, refused, installed through — and it is the verifier's to enforce. The
second is about the LIFECYCLE — regenerated with the referent, and any entry
without one declared uncovered — and it is a human's to honour at a bump, with
the verifier's first-run refusal as its enforcement.

## 5. Alternatives inside the chosen option

- **Generating the lockfile from the tarball URL rather than the exact version.**
  Both were available (`"@fission-ai/openspec": "1.12.0"` versus the
  `https://registry.npmjs.org/…/openspec-1.12.0.tgz` URL as the dependency spec).
  The exact version was chosen because the resulting lockfile is the one an
  ordinary `npm install` in an ordinary project would produce — same `resolved`,
  same `integrity` — so the file is reviewable against a reader's own experience
  rather than being a shape only this repository writes. The URL form would have
  bound the artifact more tightly *in the lockfile*; that binding is supplied
  instead by the verifier REFUSING unless the lockfile's entry carries the pin's
  own integrity, which is a stronger check because it is code rather than a
  string in a file.
- **One lockfile per pinned entry versus one per pin.** One per entry, and the
  rollback's is declared missing (§ 6). A single rewritten-in-place lockfile
  would make the rollback silently install the wrong tree.
- **A `--verify-only` mode to check the lockfile without validating.** Not
  added, not considered further: the verifier's own docstring forbids it, the
  prohibition is a ratified contract decision rather than a style preference, and
  `test_there_is_no_verify_only_mode` asserts the absence. Nothing here reopens
  it.

## 6. What stays open, named rather than discovered

### 6.1 Trust on first use

The 79 integrity values in the committed lockfile were recorded from **what the
registry served when the file was generated**, on 2026-09-08. This pin asserts
that every later install matches THEM; it does not assert that they were the
right bytes on the day they were captured. That is the trust every lockfile in
the world rests on and it is a real limit, not a formality: the CLI's own entry
is corroborated by `integrity:` in the pin — a value independently re-measured
from the registry by #677 and recomputed on every run — and **the other 79 are
corroborated by nothing outside the lockfile itself**.

What that buys is still large and it is worth stating precisely: the closure is
now FIXED and AUDITABLE rather than VERIFIED-FROM-FIRST-PRINCIPLES. A change to
any of the 79 is now a diff in a governed file with an author and a review, where
before it was an invisible consequence of a caret and a clock. Closing the
remaining gap needs an independent attestation of those packages — a provenance
attestation, a mirrored registry, or a second capture from an independent
network path compared against this one — and none is proposed here.

### 6.2 The regeneration obligation at every bump

A version bump now moves **five** things and not four: `version`, `integrity`,
`shasum`, `tarball` **and** a regenerated lockfile with `lockfile_integrity:` and
`lockfile_packages:` re-recorded. This is written into the pin's header as part
of the bump procedure and into the verifier's remediation trailer, with the
regeneration command spelled out.

**It is enforced rather than remembered**, which is the property that matters: a
bump that moved the referent and left the lockfile behind would leave the
lockfile's entry for the package carrying the OLD integrity, and the first run of
the verifier after that bump refuses `pin-lockfile-mismatch` —
`LOCKFILE REFERENT DISAGREEMENT`, naming both values. The pull request that
forgets cannot merge, because `openspec-cli-pin` is a required check.

### 6.3 The rollback entry has no lockfile, and says so

`rollback:` for `1.2.0` carries a `dependency_closure:` statement declaring
itself UNCOVERED. No lockfile is committed for `1.2.0` and none is generated
speculatively, because a lockfile generated today would record the versions the
caret ranges resolve to TODAY — a fiction of reproducibility dressed as a record
of one — and nothing would ever install through it, so its correctness would be
checked by no run and would rot in place. That is the same argument the estate
makes everywhere else about a value nothing verifies.

The consequence is stated rather than left to be met under pressure: **a pin
returned to `1.2.0` by moving the four referent fields alone is REFUSED on its
first run**, not installed unlocked. That is the fail-closed answer and it is the
right one — a rollback is already a governed edit to this file (its
`dispositions:` must be dropped in the same act, which the block already says) —
but it does mean the rollback is a change to author and not a revert to apply.
Whoever takes it authors a `1.2.0` lockfile in the same commit.

### 6.4 Smaller things, listed so they are not surprises

- **`npm ci` needs the registry or a warm npm cache.** It is not an offline
  install, and neither was the install it replaces — the nine caret-ranged
  dependencies were always fetched. `--tarball` is documented accordingly.
- **The lockfile is npm's format, so this closure is npm-shaped.** A future
  pinned product distributed through another package manager would need that
  manager's lockfile; the requirement is written in terms of "the resolution
  format the product's own package manager consumes" rather than naming npm, so
  the capability admits it without an amendment.
- **`lockfileVersion: 3` is asserted by a test.** npm's lockfile format has
  changed before. A future npm that writes a different version will fail that
  test on a developer's machine at regeneration time, which is where the
  decision belongs.
- **80 packages, not 94.** The brief this lane worked from recorded 94 as a
  prior measurement. Re-measured on 2026-09-08 three independent ways — the
  existing `npm install --global` install path, the generated lockfile's
  `node_modules/` entry count, and a walk of the tree `npm ci` produced — all
  three read **80**, and `npm` itself printed `added 80 packages` for both
  install shapes. 80 is what is recorded and what is checked.
