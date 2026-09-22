---
code_surface: none — MEASURED, not assumed, against `main` `ac50d70d`, the commit this packet was authored on. The delta is requirement prose, and the running code it describes ALREADY BEHAVES THIS WAY; not one character of a verifier, a validator, a test or a contract moves in this pull request. Evidence, each check run rather than asserted: (1) `grep -n "pinned_by_commit_only" scripts/verify-opendox-pin.py scripts/verify-openxdox-pin.py` returns TWO lines and BOTH are module-docstring PROSE describing the openXwallet pin's shape (`verify-openxdox-pin.py:19` and `:75`) — neither verifier READS the key, and `files` is read by neither; (2) both verifiers key the whole surface on `digest_definition: sorted-ls-tree-r-v1` plus `digests.tree_sha256` and enumerate closed refusal vocabularies that contain NO code for a missing per-file list — `verify-opendox-pin.py:137-143` is six codes (`opendox-pin-tag-only`, `-submodule-uninitialized`, `-gitlink-mismatch`, `-checkout-mismatch`, `-digest-mismatch`, `-lockstep-mismatch`) and `verify-openxdox-pin.py:158-163` is the same five without the lockstep one; (3) the two verifiers that DO read the key read it with an absent-is-empty default — `pin.get("pinned_by_commit_only") or []` at `verify-openxwallet-pin.py:443-452` and `validate-openreposhape-pin.py:487-495`, transcribed by doc-health's own adapter at `scripts/doc_health/pin_shapes.py:187-201`, whose `_is_path_only_list` admits EVERY falsey value as empty — so absence is already lawful there too and this amendment widens nothing in them; (4) the tested shape IS the whole-tree one: `tests/opendox_pin/test_opendox_pin_verifier.py:339-340` and `tests/openxdox_pin/test_openxdox_pin_verifier.py:264-265` build their pins from `digest_definition` plus `digests.tree_sha256` with no per-file key at all, and `python3 -m pytest tests/opendox_pin tests/openxdox_pin -q` reads **105 passed** at this head. (5) EVERY `contracts/*-pin.yaml` IN THIS REPOSITORY WAS READ, so the exclusivity the amendment states is checked against the estate's real pins rather than asserted: `opendox` and `openxdox` carry a `tree_sha256` and NEITHER list; `openreposhape` and `openxwallet` carry `files:` + `pinned_by_commit_only:` and NO tree digest; `openspec-cli` and `review-lane` carry none of the three — **no pin carries a whole-tree digest beside either list**, so no live pin becomes non-conformant. (6) ONE ASYMMETRY IN THE RUNNING GUARD IS REGISTERED RATHER THAN PAPERED OVER (Copilot `r4073495753`): `scripts/doc_health/pin_shapes.py`:772-775 detects the mixture only when `files` is present, so a tree pin carrying `pinned_by_commit_only:` alone is not caught, and the two tree verifiers read neither key; the scenario states the rule for BOTH halves, which is what a requirement is for, and because no pin in the estate is in that state **no code is owed by this packet** — the unreached half is registered at `tasks.md` § 5.4. THE AMENDMENT IS THEREFORE DOCTRINE-ONLY: it makes the normative text agree with a reader that has never enforced the per-file list on a source-tree pin, and a pin conformant before this lands is conformant after it. Under `release-realization` an empty code surface archives ON LANDING plus this task list rather than on merged-plus-green realization evidence.
target_release: implemented — the value `release-realization` names for a doc-only change. No contract bundle is cut, nothing under `contracts/` is edited, no `contracts/manifest.yaml` row moves, no digest inventory is recomputed and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: [split-opendox-two-layer-product]
---

# Proposal: amend-neutral-product-pin-source-tree-digest

Status: ratified
Ratified: 2026-09-22 by Brett Heap (openxFactory operator authority) — in-session, verbatim *"ratify #1140 and #1141"*, at head `ca47e2cb`; record at review/ratification-2026-09-22.md
Kind: proposal
Proposed: 2026-09-22, in lane `openxfactory-4` (display
`openXfactory-4-openDox_extraction`), on Brett Heap's ruling of the same day —
`opensoft/openxFactory` issue
[#656](https://github.com/opensoft/openxFactory/issues/656) comment
[`5777949892`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5777949892),
2026-09-22T14:04:00Z, given interactively in the lane session by multi-choice,
verbatim: **"(b) — AMEND THE CLAUSE."**
Origin: the tension Copilot review comment `r4067623184` found on
`opensoft/openxFactory#1139` and the lane's bookkeeper verified — the pin-shape
ruling `5768144952` sits against the ratified source-tree clause of
`neutral-product-pin`. **The ruling names this packet's form in so many words:**
*"it becomes its own small OpenSpec change against `neutral-product-pin`, citing
5768144952, this ruling, and Copilot `r4067623184`."*

**THE DECISION IS BRETT HEAP'S AND THE ENCODING IS THIS LANE'S.** This packet
makes no judgment the ruling did not make. The word that COMMISSIONED the
amendment (`5777949892`) and the word that RATIFIES this packet
(`5779511063`, 2026-09-22T15:45:54Z, verbatim *"ratify #1140 and #1141"*) are two
separate acts, and both are Brett Heap's.

**THE RATIFIED BASELINE IS `ca47e2cb` AND THE HEAD IS NOT, WHICH IS DISCLOSED
RATHER THAN SMOOTHED.** `9f82caeb` was committed at **15:45:53Z**, ONE SECOND
before the word, and pushed around it — so it was in flight at the moment of
ratification and Brett Heap cannot have read it. **It changed NORMATIVE text**:
it reversed the runtime exclusion that `ca47e2cb` carried, on a measurement
showing that exclusion would have made `contracts/opendox-pin.yaml` itself
non-conformant. The change is a correction in the ratified direction and not a
new decision — but it is requirement text, and requirement text moved after a
ratify word is not the authoring lane's to absorb. **RE-RATIFICATION AT
`9f82caeb` IS REGISTERED AS OWED** at `tasks.md` § 1.3 and in the ratification
record § 3.

## Why

**Two ratified readings in one capability disagree, and the pins the estate
actually carries obey the second.**

The requirement *An external neutral product is pinned by commit and digest,
never by tag* opens by obliging a consuming pin to carry "a per-file `sha256`
for every artifact the product's own manifest digests per file, and
`pinned_by_commit_only:` for every artifact the product content-addresses by
commit alone". Three paragraphs later, for a product distributed as a published
artifact, the same requirement reasons the obligation away in its stronger form:
those two lists exist only because "a commit is not a digest a consumer can
compare a single file against, so the surface must be ENUMERATED for
completeness to be checkable at all", whereas **"ONE digest addresses EVERY byte
inside it, so no member can be undeclared and none can be added or altered
without changing the referent"** — and the obligation is therefore "DISCHARGED
MORE STRONGLY here rather than waived".

**That reasoning does not depend on the medium, and the estate had already
applied it to a source tree.** `contracts/openxdox-pin.yaml` and
`contracts/opendox-pin.yaml` each pin an assembly ROOT by commit plus a
whole-tree `sorted-ls-tree-r-v1` digest and carry neither list, and each header
gives the published-artifact paragraph as its reason, quoting it. On 2026-09-21
the condition those headers had deferred against actually fired: at openDox
`dc7aa08f` the product's own `contracts/manifest.yaml` carried a non-empty
`entries:` for the first time, so the per-file obligation had members. The
question went up as a `RULING NEEDED` (`#656` comment `5768088579`) and Brett
Heap answered **"(b) for the pin shape, keep going"** (`5768144952`): the lists
stay deferred, on the whole-tree digest's own strength.

**What that ruling settled was the PIN FILES. It did not settle the NORMATIVE
TEXT, and until it is settled the corpus holds a rule and an unwritten
exception.** Copilot found exactly that on the archive pre-stage of
`split-opendox-two-layer-product` (`r4067623184`), the bookkeeper verified it,
and Brett Heap ruled the remedy by multi-choice on 2026-09-22: **amend the
clause** rather than record an exception beside it — *"It leaves ONE rule in the
corpus rather than a rule and an exception, and its reasoning is already written
in the requirement three paragraphs down."*

## What changes

**ONE `## MODIFIED` block, on ONE requirement, adding ONE paragraph and FIVE
scenarios. No unit the requirement already carries is edited.**

1. **The equivalence, stated with its ground.** A pin of a SOURCE TREE that
   declares a whole-tree digest definition and records a digest over the ENTIRE
   tree of the commit it names discharges the per-file `sha256` /
   `pinned_by_commit_only:` obligation, and **such a pin carries NEITHER list**
   (see 2). The
   paragraph says WHAT MAKES THEM EQUIVALENT rather than merely asserting it: a
   whole-tree digest covers every file in the tree and therefore SUBSUMES any
   list of them, which is the published-artifact paragraph's own reasoning
   reaching a source tree unchanged.
2. **The two forms are ALTERNATIVES, not a menu.** Such a pin carries NEITHER
   list, in the published-artifact clause's own words. This is not tidiness:
   `scripts/doc_health/pin_shapes.py`:763-775 already REFUSES a record carrying
   both a whole-tree `digests.tree_sha256` and a `files:` list, naming both
   shapes tried, so text admitting the mixture would disagree with a guard that
   is already running. *(Raised by Copilot `r4073364832`; the wording was `MAY
   then be absent` and is now the exclusion the guard enforces.)*
3. **The boundary, stated so it cannot be read wider.** The equivalence is about
   WHICH FORM the digest obligation takes and never about WHETHER digests are
   owed. An enumeration remains lawful and remains OWED where no whole-tree
   digest is recorded — this admits a second form and retires neither the first
   nor any pin carrying it (`contracts/openxwallet-pin.yaml`'s eight `files:`
   digests are untouched and stay conformant). **And it does not reach a pin the
   runtime-deployment clause governs**: for a product carrying a schema and
   ordered migrations that clause stands unmodified, its trusted referent
   unchanged, and whether a whole-tree digest may discharge the obligation THERE
   is left unopened rather than answered by implication. *(Raised by Copilot
   `r4073177274`, which was right that saying the clause is "untouched" did not
   settle whether the new scope reached the pins it governs. It now does not.)*
   A pin recording NEITHER form has discharged nothing.
4. **Five scenarios** — the conformant whole-tree pin; the pin carrying BOTH
   forms, refused; the pin recording neither, refused; **the runtime product's
   pin, whose whole-tree digest DOES discharge the obligation while every
   deployment obligation stays owed in full**; and the misreading that cites the
   equivalence as permission to skip a digest, refused.

### A side effect worth naming: the capability stops being silent

`scripts/doc_health/pin_shapes.py`:764-770 records, in its own words, that
"`neutral-product-pin`'s ratified text is SILENT on the whole-tree shape — the
spellings `digest_definition`, `digests` and `tree_sha256` occur nowhere under
`openspec/specs/`", and falls back to the capability's fail-closed rule for want
of text. **This amendment ends that silence**: it is the first promoted text to
name the form the guard has been judging. The guard is not changed — it already
does what the text will now say.

### The block is written over `split-opendox-two-layer-product`'s outcome

That packet holds an active `## MODIFIED` block on this same requirement,
ratified 2026-09-05, adding the runtime-deployment clause and two scenarios. A
block written over canon-as-promoted would drop them the moment that packet
archived. So this one carries the basis's outcome whole — all seven of its
scenarios, its runtime clause and its own per-requirement record — and marks its
two additions in place, which is the form the basis itself used one link up this
chain over `add-openspec-cli-pin`. `sequenced_after:` declares the ordering and
this section is the reference the `modified-block-currency` family reads.

## Impact

- **Specification:** `neutral-product-pin` — one MODIFIED requirement.
- **Code:** none. See the `code_surface:` measurement above: 105 tests pass
  unchanged, and no verifier reads either list key for a source-tree pin.
- **Contracts:** none. `contracts/opendox-pin.yaml` and
  `contracts/openxdox-pin.yaml` are already in the shape this amendment admits,
  and their headers already cite the reasoning it promotes — **this packet edits
  neither**, because what the pin files carry was settled and executed by
  `5768144952` and this one settles only the normative text.
- **Registered, not fixed:** the required-check requirement's scenario *The
  pinned reader runs before the pin is verified*
  (`openspec/specs/neutral-product-pin/spec.md`:147-149) conditions on the
  per-file digests and the `pinned_by_commit_only:` set, which a whole-tree pin
  does not carry. **The gap predates this packet** — the two pins have carried
  the whole-tree form since they were filed — and amending a SECOND requirement
  is beyond a commission that names one clause, so it is registered at
  `tasks.md` § 5.3 for a successor rather than swept in here. *(Copilot
  `r4073110728`.)*
- **Registered, not fixed (2):** `pin_shapes.py`:772-775 detects the both-forms
  mixture only when `files` is present, so a tree pin carrying
  `pinned_by_commit_only:` alone is not caught. **No pin in the estate is in
  that state** (every `contracts/*-pin.yaml` was read), so no code is owed here
  and `code_surface: none` stands; the unreached half is registered at
  `tasks.md` § 5.4. *(Copilot `r4073495753`.)*
- **The corpus after:** one rule, not a rule and an exception.
