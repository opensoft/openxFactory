# Design: add-openspec-cli-pin

Status: draft

Nine decisions, each with the alternative that was rejected and why. The
proposal's § Authoring decisions is the index; this is the argument.

## D1 — `kind: pinned_contract_manifest`, reused unchanged

**Decided:** reuse the ratified kind.

**Rejected:** a new `kind: openxfactory_openspec_cli_pin`. Both sibling pins
rejected the equivalent for the same reason and it is not weaker here: the
`<consumer>_<product>_pin` template governs DESCENDANTS, and openxFactory is not
a descendant of a Node package. Only the DISTRIBUTION FORM is new — a published
artifact rather than a git tree — and a new kind for a new medium would make
`neutral-product-pin` a catalogue of shapes instead of a statement about
direction.

## D2 — the referent is the tarball's SHA-512; the version is a label

**Decided:** `revision_kind: package_integrity`, `integrity:` as the trusted
referent, `version:` recorded as a label.

**Rejected:** pin on the version string alone, on the ground that npm versions
are immutable. They are *conventionally* immutable, and that is the problem: the
immutability is a REGISTRY POLICY, administered by an operator, with an unpublish
window an operator can act inside. `neutral-product-pin` exists precisely to
separate "a name somebody keeps stable" from "an address nothing can move", and
adopting a policy as a referent would be conceding the distinction in the first
pin that tested it.

**Also rejected:** record the integrity but check only the version. That is the
`openreposhape` pin's own rejected shape — a referent recorded in prose and
verified by nothing — and it verifies green against whatever bytes arrive.

## D3 — the verifier and the consumer entrypoint are one file

**Decided:** `scripts/validate-openspec-cli-pin.py` verifies the pin AND runs
the validation.

**Rejected:** a verifier beside a separate wrapper, mirroring the siblings'
verifier-only shape. That shape is right for them: openRepoShape's mechanics run
in the projects that fork the standard, so the verifier has nothing to invoke.
Here the pinned tool IS invoked, on every governed act, and a verifier nobody is
obliged to call standing beside a bare `openspec` invocation is exactly the state
this packet exists to end. Making them one file makes "run the validation" and
"prove which tool ran" the same act, which is the only way the obligation is
self-enforcing.

## D4 — `npm pack`, not a direct HTTPS GET

**Decided:** fetch through `npm pack <package>@<version>`.

**Rejected:** `urllib` against the `tarball:` URL, which would have kept the tool
free of a package-manager dependency. It was rejected because it would create a
SECOND resolution path: the verifier could agree with the pin over bytes fetched
privately while every ordinary `npm install` in the estate received something
else, and the gate would report green about an artifact nobody runs. Going
through npm means the bytes checked are the bytes an ordinary install receives.
The digest is recomputed regardless of which path produced the file, so nothing
is trusted about `npm` beyond "it fetched something".

## D5 — three exit codes, not two

**Decided:** `0` clean, `1` the pin held and the pinned CLI reported failures,
`2` any refusal.

**Rejected:** the siblings' deliberate two-valued shape. Their reasoning — "a
stale pin and an unresolvable tree are the same answer to *may this pull request
proceed*, and a two-valued failure invites a workflow that treats one of them as
a warning" — is sound for a tool that asks one question. This tool asks two: WHICH
tool adjudicates, and what did it say. Collapsing them would hide the ordinary
finding (fix your delta) inside the extraordinary one (the pin cannot be
trusted), which are not remedied in the same place or by the same person. Both
codes are non-zero, so a workflow that treats non-zero as failure — which is
every workflow — is unaffected.

## D6 — no `--verify-only`; `--strict` is a no-op and `--no-strict` does not exist

**Decided:** every invocation opens a governed surface, and every invocation is
strict.

**Rejected:** a `--verify-only` convenience for "just check the pin". It is
precisely the target-less green check `neutral-product-pin` forbids — "a
self-test that opens no governed surface is a green check that verified nothing"
— and a gate would eventually be pointed at it. `--strict` is accepted and
ignored so that a habitual `--all --strict` reaches the entrypoint unchanged;
there is no way to drop strictness, because a non-strict pass is not the act this
pin governs.

## D7 — the cache holds installs, never verdicts

**Decided:** re-fetch and re-hash the artifact on EVERY run; reuse only the
install directory, which is named by the verified content address and carries a
stamp recording it.

**Rejected:** cache the verification result and skip the fetch on a hit. The
fetch is cheap — npm serves a 200 KB artifact from its own local cache — and the
`npm install` is not, so the expensive half is the only half worth caching. A
cached VERDICT would mean a run inheriting a previous run's belief about what the
registry served, which is the one thing a content-addressed pin must never do.
The stamp is checked before the directory is used, so a directory built from
other bytes is rebuilt rather than reused.

## D8 — the MODIFIED delta is required, and is minimal

**Decided:** modify "An external neutral product is pinned by commit and digest,
never by tag" to admit a published-artifact referent.

**Rejected:** write the pin under the unamended grammar. The ratified text says
the pin "SHALL carry the product's COMMIT … a per-file `sha256` … and
`pinned_by_commit_only:` …". An npm package has no commit this repository
consumes and no per-file surface to enumerate. Writing the pin anyway would mean
either inventing a commit — a fabricated referent in a file whose entire purpose
is a truthful one — or claiming conformance to a requirement the file does not
meet. Both were rejected.

**Rejected:** a new capability for artifact pins. That would fork the grammar in
two over a difference of medium, and the next reader would have to know which of
two documents governs their product before they could write a pin at all.

**The block is minimal and deletes nothing:** every existing clause and all three
existing scenarios are restated unchanged, one body clause and two scenarios are
added. No reserved deletion marker is owed, because nothing is removed. The
requirement TITLE is kept: "never by tag" is still exactly what the requirement
says, and a retitle would carry an obligation to carry bullets one at a time for
no gain.

**Why the absent member lists are argued rather than waived.** The two lists
exist because a commit is not a digest a consumer can compare one file against,
so the surface must be enumerated for completeness to be checkable — hence "an
artifact that appears in neither list is an undeclared consumption". A published
tarball has no such gap: one digest addresses all 270 files, nothing can be added
without changing the referent, and there is no member the referent does not
cover. The delta says this in the grammar's own terms so the pin file is not left
asserting a licence the requirement never granted.

## D9 — `pytest-suite.yml`'s literal is a successor task

**Decided:** leave `.github/workflows/pytest-suite.yml:400` alone in this packet
and record it as task 5.1.

**Rejected:** fix it here, since the packet is literally about that literal being
the wrong instrument. It was rejected because that file is this repository's most
load-bearing required check — it carries the pinned test triple and the named
freshness verdict — and a change to how it obtains the CLI deserves its own diff
and its own green run. Riding it on this packet would mean that if anything about
it went wrong, the pin change would be what got reverted.

## Open items

* **OI-1 — the dependency closure.** The referent addresses the CLI's bytes, not
  its nine caret-ranged dependencies. Declared in the pin's header, mitigated by
  `--ignore-scripts`, not repaired. Closing it needs a lockfile the publisher does
  not ship; whether to vendor one, or to pin the resolved tree ourselves, is not
  decided here.
* **OI-2 — whether the gate becomes required.** An operator act on an
  organisation ruleset, and not this packet's to take. The workflow reports from
  the moment it lands so the check token becomes selectable.
* **OI-3 — the upgrade target.** This packet deliberately names no target
  version. 1.12.0 was measured only to size the problem, not to propose it.
