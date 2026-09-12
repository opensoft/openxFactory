# Tasks: extend-prose-tagging-target-to-pinned-capabilities

Status: draft

NO BOX BELOW IS TICKED BY THE FILING PULL REQUEST except the ones in § 2, which
record what that pull request itself did. § 1 needs Brett Heap's word, § 3 is
the later realization pull request, and § 4 is the archive act.

## 1. The ask — Brett Heap's ratification

- [ ] 1.1 **RATIFY or REFUSE the form (D-1):** an `xspec:candidate` marker's
  `target=` may be `pinned:<pin-id>/<capability>`, where `<pin-id>` is the stem
  of a `contracts/<pin-id>-pin.yaml` record. The value is EXACTLY TWO
  `[a-z0-9]+(-[a-z0-9]+)*` components separated by EXACTLY ONE `/` — measured
  to be the shape of all 62 in-tree capability ids and all six pin stems — and
  a value that fails that grammar is refused BEFORE any path is built or any
  file is read, since the marker regexes accept any non-whitespace value and
  are not the guard. For the four affected markers that
  is `target=pinned:openxwallet/openxwallet`. The form needs NO regex change —
  measured against `families.py:1308-1314`. The `xspec:supersedes` marker's
  `spec=` attribute is OUT OF SCOPE and CLOSED (D-1.1): a `spec=` value
  carrying the reserved `pinned:` prefix is refused, because the `spec=`
  grammar splits at its first `/` and no pinned parse for it is defined, and
  because no live `supersedes` marker in this repository has a stale target —
  measured.
- [ ] 1.2 **RATIFY or REFUSE the resolution rule (D-2):** the pin id must
  resolve to a VALID, COMPLETE NEUTRAL-PRODUCT pin record the RESOLUTION ROOTS
  carry — a `contracts/<pin-id>-pin.yaml` of
  `kind: pinned_contract_manifest`, five of the six today, CARRYING EVERY MEMBER
  REQUIRED BY THE RECORD SHAPE IT MATCHES — three shapes across those five, two
  of them sharing `revision_kind: commit`, so the revision kind ALONE is not the
  key — each shape's set being the SHAPE'S VERIFIER-REQUIRED SET, exactly the
  top-level members that shape's in-tree verifier refuses-when-absent
  (`openspec/specs/neutral-product-pin/spec.md:31-36`, `:46-48`, `:55-56`,
  `:62-65`, `:669-673` where that text names members; the verifier scripts where
  it is silent, which is shape (b) entirely and the published artifact's
  `package` and `binary`), pinned to those verifiers by the equivalence test of
  task 3.3(p) — this grammar enumerating no member list of its own,
  judged through a CODE-FIXED route that never executes, imports or opens a path
  a pin record selects, and resolved under the root precedence the in-tree arm
  already uses (`scripts/doc_health/families.py:1317-1321`);
  `kind: pinned_workflow` (`review-lane-pin.yaml`) is EXCLUDED,
  because it pins executable governance code and has no capability set for a
  name to be about; the capability segment is
  checked for shape and resolved further ONLY where the pin record enumerates
  capabilities — which none of the six does today, measured. The trigger is ONE
  NAMED MEMBER, reserved by this change and added to no record and no schema by
  it: a top-level `capabilities:` sequence on the pin record. The resolver
  reads that member and no other, so the dormant arm has a deterministic input
  contract rather than an intention; whether a real pin record may carry it is
  a `neutral-product-pin` question with the publisher. The weakening this
  accepts is stated plainly in D-2 and is worth a veto on its own. **THIS IS
  THE PACKET'S ONE LIVE CONSTITUTIONAL QUESTION.** Principle VII
  (`.specify/memory/constitution.md:99-103`) closes registries of capabilities
  and requires deferred features to fail closed; under arm 1 the CAPABILITY
  segment is open — `pinned:openxwallet/typo` resolves. D-2 states the
  three-way tension in full and does not resolve it by argument. Note before
  ruling: the fail-closed alternative (refuse a target whose pin record carries
  no capability enumeration) refuses all four markers this change exists to
  admit, so a REFUSE here is a refusal of the change's central mechanism rather
  than a tightening of it.
- [ ] 1.3 **RATIFY or REFUSE the stale-target rule (D-3):** when a target
  capability exits the corpus the marker either takes the pinned form or the
  block is unfenced — never silently retargeted, never silently deleted.
- [ ] 1.4 **CONFIRM the realization split (D-5):** one later pull request
  carrying resolver, tests, the four retargeted markers and the `INDEX.md`
  correction together, rather than four separate ones.

## 2. This filing — done by the pull request that carries this file

- [x] 2.1 Packet authored: `proposal.md`, `design.md`, `tasks.md`,
  `.openspec.yaml`, and `## MODIFIED` deltas against `document-lifecycle` and
  `doc-health`. The three lifecycle documents carry `Status: draft`; the two
  spec deltas carry no lifecycle header, as 299 of the 303 spec-delta files
  measured on `origin/main` at `a72f0a76` do not.
- [x] 2.2 Origin declared `kind: ad_hoc` with DRAFTING provenance
  (`proposed_by` / `proposed_on`) and NO approval pair — the lawful unapproved
  shape. The reason names Brett Heap's selection verbatim and its place.
- [x] 2.3 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.4 Per-change sweep-ledger row seeded by
  `scripts/validate-sequenced-after.py --seed-ledger`, so `--ledger-diff`
  exits 0.
- [x] 2.5 **NOTHING REALIZED.** No byte of `scripts/doc_health/families.py`
  moves, no module is added under `scripts/doc_health/`, and no byte of
  `scripts/validate-pin-registrations.py` or of any per-product pin verifier
  moves. No marker is retargeted or deleted. `ideation/staging/INDEX.md` is not
  touched. `docs/document-lifecycle.md` is not touched. The four `tag-hygiene`
  findings stand at FOUR, unchanged.
- [x] 2.6 **NO BOX ANYWHERE ELSE IS TICKED.** Item (7) of the
  `split-openxwallet-repo` archived-ledger entry (`README.md:7075` on
  `origin/main` at `177ba819`) is NOT edited by this pull request and no tick is
  claimed on it; the archived packet is not edited at all, under the
  archived-record rule.
- [x] 2.7 The two `## MODIFIED` blocks against `document-lifecycle` and
  `doc-health` each carry one clause that diverges from canon (a
  `modified-block-currency` `info` divergence apiece), so
  `tests/doc-health/test_modified_block_currency_self_gate.py`'s
  `_LEDGER_SUBJECTS` carriage ledger gains the two rows its own self-gate
  requires of them: `("extend-prose-tagging-target-to-pinned-capabilities",
  "doc-health", "Tag hygiene enforced by reference")` and
  `("extend-prose-tagging-target-to-pinned-capabilities", "document-lifecycle",
  "Prose tagging marker hygiene")`. Both rows are bookkeeping the self-gate
  requires of ANY filing that opens a divergence against a promoted block, not
  test implementation for the pinned-target arm the realization proposes.

## 3. Realization — a LATER pull request, after ratification

- [ ] 3.1 `scripts/doc_health/families.py`: teach resolution the `pinned:`
  prefix — `_resolve_capability` (line 1317) gains the arm, or a sibling
  resolver is added and `fam_tag_hygiene`'s call sites (lines 1366, 1390)
  dispatch on the prefix. The regexes at 1308-1314 DO NOT MOVE. The arm judges
  completeness through ONE of D-2's two CODE-FIXED routes — (a) preferred, a
  shared importable NON-EXECUTING shape validator for
  `pinned_contract_manifest` records, added under `scripts/doc_health/` if the
  tree carries none; or (b) a CLOSED dispatch table in the resolver's own module
  keyed by admitted pin id, under which a record's differing `verify_pin:` value
  is itself a controlled finding — and it NEVER executes, imports or opens a
  path a pin record selects, `verify_pin:` being data the arm may compare and
  MUST NOT follow. The validator HOLDS a PER-SHAPE required-member table,
  reviewed with the resolver at authoring time, whose entry for a shape is that
  SHAPE'S VERIFIER-REQUIRED SET — exactly the top-level members the shape's
  in-tree pin verifier REFUSES-WHEN-ABSENT, measured at realization from the
  verifier scripts and cited script:line per member. `neutral-product-pin`'s
  ratified text supplies members where it NAMES them (`:31-36` for the
  ENUMERATED commit shape; `:46-48`, `:62-65` and `:669-673` for the
  PUBLISHED-ARTIFACT one) and is SILENT elsewhere — on the whole-tree digest
  shape entirely (`contracts/opendox-pin.yaml:108-110`,
  `contracts/openxdox-pin.yaml:92-94`) and on the published artifact's
  `package` and `binary` — and the verifier-required set completes it rather
  than competing with it: on a landed tree every record already passes its own
  verifier, so this check defends the SIDE RUNS, and a table narrower than the
  verifier would admit there what the repository's own gate refuses. THE SHAPE
  AND NOT THE `revision_kind` IS THE KEY: two of the five records share
  `revision_kind: commit` and carry different member sets, so a table keyed on
  the revision kind alone would refuse valid records; and shape (a)'s
  product-identity member has two spellings (`submodule_path` at
  `scripts/verify-openxwallet-pin.py:194`, `source_repository` at
  `scripts/validate-openreposhape-pin.py:258`), so at the RECORD grain the
  table resolves to that record's own verifier's set. A record declaring a
  `revision_kind` the table does not recognize, and a record matching no shape
  it holds, are each an invalid pin (task 3.3(l)); the table is held to its
  verifiers by the equivalence test of task 3.3(p). It resolves the pin record under EXACTLY the root precedence
  the in-tree arm already uses — the document's own repository root, then the
  `openxFactory` root (`_resolve_capability`,
  `scripts/doc_health/families.py:1317-1321`, over `Context.repo_paths`,
  `scripts/doc_health/runner.py:39`) — invents no precedence of its own, and
  NAMES THE ROOT it resolved against in every finding the arm emits.
- [ ] 3.2 The finding text for an unresolved PINNED target names the pin
  registry, not `openspec/specs/` — the present fixed string
  (`families.py:1523-1524`, measured on `origin/main` at `177ba819`) is the
  wrong instruction for this class. The
  in-tree non-resolution arm must not judge a pinned target at all: a
  well-formed `pinned:` value exists under no `openspec/specs/` directory, so
  an unnarrowed in-tree arm would report every one of them.
- [ ] 3.3 Tests under `tests/doc-health/` (hyphen — the directory that
  exists; `scripts/doc_health/` with an underscore is the package under
  test), extending `tests/doc-health/fixtures/tag-hygiene/`, and D-2's
  CONDITIONAL arm gets BOTH
  of its cases, so the realization cannot satisfy this list while omitting the
  branch: **(a)** a resolving pinned target, under a pin record carrying no
  capability enumeration, emits nothing; **(b)** an unresolvable pin id emits a
  finding naming the PIN REGISTRY, not `openspec/specs/`; **(c)** a FIXTURE pin
  record carrying a top-level `capabilities:` sequence emits nothing for a
  capability LISTED in it; **(d)** the same fixture emits a finding naming the
  enumeration for a capability NOT listed in it — the fixture lives under
  `tests/doc-health/fixtures/`, adds no byte to any real pin record and no
  member to any schema — (c) and (d) are the positive and the negative
  of the arm that binds automatically, and without both the branch can be
  absent with this list still satisfied; **(e)** an `xspec:supersedes` marker
  whose `spec=` value carries the reserved `pinned:` prefix is REFUSED with a
  finding whose ACTION TEXT is asserted VERBATIM and states that the pinned
  form is admitted only in a candidate marker's `target=` attribute (D-1.1) —
  "a finding" is not enough here, because the generic unresolved-`supersedes`
  action would satisfy a laxer test while violating the scenario *A supersedes
  marker carries the reserved pinned prefix*, whose THEN/AND pair requires that
  sentence; **(f)** a pinned target whose record declares a kind other than
  `pinned_contract_manifest` does NOT resolve and emits a finding; **(g)** a
  pin record NAMED BY A LIVE MARKER whose `capabilities:` member is present but
  malformed — a scalar, a mapping, a null value, an EMPTY sequence, or a
  sequence carrying a non-capability-shaped item — emits a
  malformed-enumeration finding AND the pinned target naming it does not
  resolve, the record being read because the marker names it and not by any
  registry sweep, proving the fail-closed path rather
  than the "absent enumeration" fallback, with the empty sequence as its own
  case since it satisfies "a sequence of well-formed names" vacuously;
  **(h)** a pinned value that does not match the lexical grammar — an extra `/`
  segment, a dotted or traversal component such as `pinned:../x/y`, an
  upper-case or empty component — emits a malformed-pinned-target finding, and
  the test asserts NO pin-record path was constructed and NO file was read for
  it, since validating after building a path is the defect this case exists to
  prevent; **(i)** in-tree resolution is unchanged; **(j)** EVERY NEW ACTION
  STRING the arm introduces is added to the pinned table at
  `tests/doc-health/test_families.py:751` (`EXPECTED_ACTIONS`, asserted by
  `test_every_action_string_the_tag_hygiene_family_can_emit_is_pinned_verbatim`
  through `assert_actions_pinned`, which requires the expected set to equal the
  statically-present and behaviourally-emitted set EXACTLY, in both
  directions). That table is where this family's remedy wording is held, so a
  new arm that does not update it turns the suite red — and it is also what
  stops the pin-registry remedy of (b) and the candidate-`target=` remedy of
  (e) from drifting back to the in-tree string later; **(k)** a
  `contracts/<pin-id>-pin.yaml` that EXISTS but is corrupt — invalid YAML, a
  non-mapping document, or a mapping with no `kind` — becomes a controlled
  tag-hygiene finding and the pinned target naming it does not resolve, with
  the run COMPLETING rather than raising out of the family, one case per shape:
  the resolver reads this registry file, so a corrupt record must not escape
  the family and abort doc-health; **(l)** an INVALID PIN — a record
  declaring `kind: pinned_contract_manifest` that matches NO admitted RECORD
  SHAPE, or matches one and is INCOMPLETE against the members THAT SHAPE
  requires — emits a finding NAMING THE SHAPE TRIED, THE FAILING MEMBER AND THE
  ROOT IT RESOLVED AGAINST and does not resolve the target. THE MATRIX IS SPLIT
  BY SHAPE AND BY FIELD, because the five `pinned_contract_manifest` records on
  `origin/main` carry THREE shapes and two of them share
  `revision_kind: commit`: a matrix keyed on the revision kind alone, or one
  judging `files:` and `pinned_by_commit_only:` by a single rule, would REJECT
  VALID RECORDS this repository ships. The cases, and they reach SECONDARY
  fields rather than top-level referents alone. FIRST the referent cases a
  kind-only test leaves open, since a resolver could check for the presence of
  `revision_kind` and never check what it points at: a record carrying only
  `kind: pinned_contract_manifest`; a record declaring `revision_kind: commit`
  with no `commit`; a record declaring `revision_kind: package_integrity` with
  no `integrity`. THEN, per shape. SHAPE (a), THE ENUMERATED COMMIT PIN
  (`contracts/openxwallet-pin.yaml:70,104`,
  `contracts/openreposhape-pin.yaml:134,201`;
  `openspec/specs/neutral-product-pin/spec.md:31-36`) — one case per FIELD and
  per FORM, the two lists being of different forms: a `files:` entry that is a
  mapping carrying NO `sha256` is REFUSED; a `pinned_by_commit_only:` entry that
  is a PATH-ONLY STRING is ACCEPTED, this being the valid form, and a test
  demanding a digest of it would reject `contracts/openxwallet-pin.yaml:104-110`
  itself; a `pinned_by_commit_only:` entry that is a MAPPING is REFUSED as the
  wrong form; plus each list absent, and each a non-sequence. SHAPE (b), THE
  WHOLE-TREE DIGEST COMMIT PIN (`contracts/opendox-pin.yaml:92-93,108-110`,
  `contracts/openxdox-pin.yaml:76-77,92-94`) — the POSITIVE case FIRST, since
  omitting it is how this shape came to be missed: a record with `commit`,
  `revision_kind: commit`, `submodule_path`, `digest_algorithm`,
  `digest_definition` and a `digests` mapping carrying `tree_sha256` and
  NEITHER per-file list RESOLVES, and the absent lists are not reported as
  missing members; then one MISSING and one MALFORMED case for each of that
  shape's SIX verifier-required members — `submodule_path`
  (`scripts/verify-opendox-pin.py:215`), `revision_kind` (`:226`), `commit`
  (`:234`), `digest_algorithm` (`:246`), `digest_definition` (`:253`) and
  `digests` (`:262`) with its nested `tree_sha256` (`:269`), the digest
  malformed case being a value that is not the 64-hex form the two records
  carry and the two definition members mattering because each verifier refuses
  a value other than the one it implements; then the MIXED case — a record carrying
  both `digests.tree_sha256` and a `files:` list — REFUSED as matching no
  admitted shape, `neutral-product-pin`'s ratified text being SILENT on the
  whole-tree shape (the spellings `digest_definition`, `digests` and
  `tree_sha256` occur nowhere under `openspec/specs/`) so that no text admits
  the mixture and the fail-closed rule (`:89`) governs. SHAPE (c), THE
  PUBLISHED-ARTIFACT PIN (`contracts/openspec-cli-pin.yaml:282,289,297,299,308,328-330,370`;
  `:46-48`, `:62-65`, `:669-673`) — one MISSING and one MALFORMED case for EACH
  of its NINE verifier-required members, every one measured from
  `scripts/validate-openspec-cli-pin.py`: `revision_kind` (`:592`), `version`
  (`:601`), `integrity` (`:619`), `shasum` (`:646`), `package` (`:658`),
  `lockfile` (`:698`), `lockfile_integrity` (`:708`), `lockfile_packages`
  (`:731`) and `binary` (`:748`). `lockfile_integrity` and `lockfile_packages`
  because `:669-673` obliges the digest over the lockfile's exact bytes and the
  size of the tree it locks BESIDE the committed file, so a set naming
  `lockfile` alone leaves them unchecked; `package` and `binary` because the
  ratified text does not reach them at all and the verifier refuses a record
  without either, so a set read from the text alone would be weaker than the
  gate. AND a NEGATIVE case per shape for the members that are NOT
  verifier-required: an absent `pinned_by_commit_only:` under shape (a) and an
  absent `dispositions:` under shape (c) each RESOLVE, both verifiers reading
  them with an absent-is-empty default
  (`scripts/verify-openxwallet-pin.py:443`,
  `scripts/validate-openreposhape-pin.py:487`,
  `scripts/validate-openspec-cli-pin.py:801-803`), so a table that demanded
  them would refuse records the gate admits. AND the UNKNOWN cases: a record
  declaring a `revision_kind` the table does not recognize, and a record whose
  member set matches no shape at all. The case that names the hole this list
  closes is `contracts/evil-pin.yaml` carrying `kind`, `revision_kind: commit`
  and a well-formed `commit` and NOTHING ELSE: it satisfies a top-level-referent
  check, it matches NEITHER commit-pinned shape, and it MUST NOT resolve a
  pinned target. Any later shape, revision kind or member `neutral-product-pin`
  admits owes a case here on the same rule and arrives through THAT capability's
  text — or, where that text is silent and a record shape is realized ahead of
  it, through a measurement of the records recorded beside the table — rather
  than through a list restated in this family, so a file added to `contracts/`
  cannot admit an arbitrary pinned target by carrying a label or a partial
  member set; **(m)** the candidate pin path is RESOLVED and refused unless it stays
  inside THE RESOLVING REPOSITORY ROOT'S `contracts/` directory, with FOUR escape
  cases and not one. TWO are the CANDIDATE's: a symlinked
  `contracts/<pin-id>-pin.yaml` resolving OUTSIDE the repository, and one
  resolving INSIDE the repository but OUTSIDE `contracts/` (for example
  `contracts/foo-pin.yaml -> ../openspec/specs/…`), each refused rather than
  followed, with a symlink/escape fixture per case. TWO MORE ARE THE BOUNDARY'S
  OWN, and they are not reachable by any candidate check: `<root>/contracts`
  ITSELF a symlink to another directory INSIDE the repository, and itself a
  symlink to one OUTSIDE it. An implementation comparing the candidate against
  `(root / "contracts").resolve()` ACCEPTS AND READS a file outside the lexical
  registry in both, the redirection having moved the boundary rather than been
  caught by it. So the arm FIRST requires that root's `contracts` to be a REAL,
  NON-REDIRECTING DIRECTORY INSIDE THE ROOT — is a directory, is not a symlink,
  resolved path equals lexical path — CHECKED BEFORE ANY CANDIDATE IS RESOLVED;
  each of the two cases asserts that the pinned arm REFUSES FOR THAT ROOT with a
  controlled finding NAMING THE ROOT and that NOTHING IS READ (asserted on the
  read surface, not by reading a finding text), and a fifth, POSITIVE case
  asserts that an ordinary real `contracts/` directory passes the precondition
  and resolves normally. The
  helper the arm calls SHALL RECEIVE THE RESOLVING REPOSITORY ROOT AS A PARAMETER
  and check the resolved candidate against THAT root's `contracts/` boundary
  BEFORE any read. `resolve_in_tree`
  (`scripts/validate-pin-registrations.py:237-267`) is the repository's
  containment dialect and the arm reuses it rather than inventing a second one,
  but NOT AS WRITTEN: it resolves against a module-global `ROOT` and asks only
  `resolved.is_relative_to(ROOT)`, so it answers the REPOSITORY question and not
  the `contracts/` one — the second escape above passes it — and a module-global
  root cannot speak for the doc-health fixture and aggregate roots this family
  runs against. So the realization parameterizes that helper or extracts a
  shared one both call, and the two cases above are what prove it;
  **(n)** NON-USE, asserted directly: a record whose
  `verify_pin:` member names an ARBITRARY IN-TREE PATH has that path NEVER
  opened, imported or run — asserted by instrumenting the read/import/exec
  surface, not by reading a finding text, since the boundary is that the path is
  not touched — and the record's verdict is UNCHANGED by that member's value: a
  record complete for its record shape still RESOLVES, since `verify_pin:` is
  neither part of the required shape nor a resolution prerequisite, and a test
  that refused such a record would encode the opposite of D-2 and reject valid
  pins. ONLY where the realization picks D-2's form (b) does a `verify_pin:`
  value that differs from the module's dispatch-table entry emit the
  disagreement finding, which is a case of route (b) alone and is not asserted
  against route (a); **(o)** the CROSS-REPOSITORY case, an aggregate
  fixture with TWO roots: (i) the pin record exists only in the `openxFactory`
  root and a document of the other repository names it — the target resolves by
  the fallback and the finding or log NAMES that root; (ii) both roots carry a
  record for the same `<pin-id>` — the DOCUMENT'S OWN repository's record is the
  one read; and (iii) the SINGLE-ROOT NEGATIVE, the same document read by a
  `--single-repo` run of its own repository, where the record exists only in the
  `openxFactory` root: the target does NOT resolve, the finding NAMES the one
  root searched, and the pass does not widen its root set to reach the record.
  (iii) is what the arm guarantees and (i) is not its contradiction: what is
  unchanged across scopes is the ORDER, not the outcome, the aggregate run
  simply having a second root. Without (o) the arm can pass every single-root
  test and still invent a precedence of its own, and without (iii) a reader
  could take (i) as a promise that a marker resolves identically however
  doc-health was invoked; **(p)** THE EQUIVALENCE TEST THAT PINS THE PER-SHAPE
  TABLE TO THE VERIFIERS, over each real `pinned_contract_manifest` record in
  `contracts/` and not over fixtures alone: for EVERY top-level member `m` of
  the record, the shape's verifier REFUSES the record with `m` removed IF AND
  ONLY IF `m` is in the table for that record's shape. Both directions are
  asserted, because they fail differently: a table NARROWER than its verifier
  admits, on a fixture or side run, a record the repository's own required check
  refuses — which is the defect this arm exists to close — and a WIDER one
  refuses a record that gate admits. The verifier is exercised through its own
  shape-reading entrypoint on an in-memory copy of the record with one member
  deleted, NOT by running it against the network or a checkout: the question is
  which members it REFUSES-WHEN-ABSENT, which its shape guards answer before any
  fetch or `git` call. The measured baseline the test starts from is the table
  of design D-2 — shape (a) `revision_kind`, `commit`, `files` plus exactly one
  product-identity member (`submodule_path` OR `source_repository`); shape (b)
  `submodule_path`, `revision_kind`, `commit`, `digest_algorithm`,
  `digest_definition`, `digests`; shape (c) the nine of
  `scripts/validate-openspec-cli-pin.py` — and the test is what keeps that
  baseline true as either side moves, rather than a comment asserting it was
  true once.
- [ ] 3.4 `docs/document-lifecycle.md` Prose Tagging Markers section: the new
  target form beside the existing `<capability>` bullet, its scope (candidate
  `target=` only, per D-1.1), and D-3's stale-target sentence.
- [ ] 3.5 Retarget the four markers to `target=pinned:openxwallet/openxwallet`
  — `ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`
  lines 222, 242, 280 and
  `ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md`
  line 107. Line numbers re-measured at that branch's tip, never carried from
  here on trust.
- [ ] 3.6 Correct `ideation/staging/INDEX.md:2262-2265`, which still describes
  three `openxwallet` blocks as "all resolving" and has been false since
  2026-08-28.
- [ ] 3.7 Evidence: a `--single-repo` doc-health run over the realization tree
  showing the four `tag-hygiene` findings at ZERO and `New regressions: 0`, and
  the green required `pytest-suite` run, both cited at the TREE grain.

## 4. Archive — a separate act on Brett Heap's word

- [ ] 4.1 Archive via `scripts/proposal-support.py` (never bare `openspec`),
  on merged-plus-green realization evidence per `release-realization`, since
  this packet's `code_surface` is non-empty.
- [ ] 4.2 The archived-ledger entry records that item (7) of
  `split-openxwallet-repo`'s successor register is discharged by this change,
  naming this change id and its realization pull request.
- [ ] 4.3 `openspec/specs/document-lifecycle/spec.md` and
  `openspec/specs/doc-health/spec.md` carry the promoted MODIFIED requirement
  text verbatim, per `promotion-fidelity`.
