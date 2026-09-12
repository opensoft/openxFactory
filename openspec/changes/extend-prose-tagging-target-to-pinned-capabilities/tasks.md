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
  resolve to a NEUTRAL-PRODUCT pin record this repository carries — a
  `contracts/<pin-id>-pin.yaml` of `kind: pinned_contract_manifest`, five of
  the six today; `kind: pinned_workflow` (`review-lane-pin.yaml`) is EXCLUDED,
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
  `doc-health`. Every document carries `Status: draft`.
- [x] 2.2 Origin declared `kind: ad_hoc` with DRAFTING provenance
  (`proposed_by` / `proposed_on`) and NO approval pair — the lawful unapproved
  shape. The reason names Brett Heap's selection verbatim and its place.
- [x] 2.3 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.4 Per-change sweep-ledger row seeded by
  `scripts/validate-sequenced-after.py --seed-ledger`, so `--ledger-diff`
  exits 0.
- [x] 2.5 **NOTHING REALIZED.** No byte of `scripts/doc_health/families.py`
  moves. No marker is retargeted or deleted. `ideation/staging/INDEX.md` is not
  touched. `docs/document-lifecycle.md` is not touched. The four `tag-hygiene`
  findings stand at FOUR, unchanged.
- [x] 2.6 **NO BOX ANYWHERE ELSE IS TICKED.** Item (7) of the
  `split-openxwallet-repo` archived-ledger entry (`README.md:6828-6832`) is NOT
  edited by this pull request and no tick is claimed on it; the archived packet
  is not edited at all, under the archived-record rule.

## 3. Realization — a LATER pull request, after ratification

- [ ] 3.1 `scripts/doc_health/families.py`: teach resolution the `pinned:`
  prefix — `_resolve_capability` (line 1317) gains the arm, or a sibling
  resolver is added and `fam_tag_hygiene`'s call sites (lines 1366, 1390)
  dispatch on the prefix. The regexes at 1308-1314 DO NOT MOVE.
- [ ] 3.2 The finding text for an unresolved PINNED target names the pin
  registry, not `openspec/specs/` — the present fixed string
  (`families.py:1367-1368`) is the wrong instruction for this class. The
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
  finding (D-1.1); **(f)** a pinned target whose record declares a kind other than
  `pinned_contract_manifest` does NOT resolve and emits a finding; **(g)** a
  pin record whose `capabilities:` member is present but malformed — a scalar,
  a mapping, a null value, an EMPTY sequence, or a sequence carrying a
  non-capability-shaped item — emits a malformed-enumeration finding AND the
  pinned target naming it does not resolve, proving the fail-closed path rather
  than the "absent enumeration" fallback, with the empty sequence as its own
  case since it satisfies "a sequence of well-formed names" vacuously;
  **(h)** a pinned value that does not match the lexical grammar — an extra `/`
  segment, a dotted or traversal component such as `pinned:../x/y`, an
  upper-case or empty component — emits a malformed-pinned-target finding, and
  the test asserts NO pin-record path was constructed and NO file was read for
  it, since validating after building a path is the defect this case exists to
  prevent; **(i)** in-tree resolution is unchanged.
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
