Reviewer role: Adversary Engineer (council review, read-only) — 2026-08-22
Subject proposal: openspec/changes/add-wallet-carried-review-authority/proposal.md

# Adversary Engineer — `add-wallet-carried-review-authority`

Read: the proposal (921 lines), both alignment reports, `openxwallet` +
`openxwallet-agent-profile` + `roles-authority-model` specs, all of
`contracts/openxwallet/` including 30 negative fixtures,
`scripts/validate-openxwallet.py` (1466 lines), the active
`add-substantive-review-lane` delta, codexFactory `hermes/domain/`, and
`council_orchestration.py` / `domain_content_set.py` in hermes-install.

The proposal is unusually honest — it names LS-A3 as its founding lesson and
quotes the caveats that cut against it. My findings are that it commits the
LS-A3 error three more times, at higher altitude, on the three controls it
treats as already-existing.

---

## 1. The one surviving boundary has its decision OUTSIDE the tree and its FACTS inside it — and its content channel is not wired at all. HIGH

**Concern.** §3's whole claim is "For convening admission the Hermes runtime
already provides it… the checker is already outside the checked tree, by
deployment rather than by decree." Neither half survives contact with the
runtime.

**Evidence.**

*(a) The runtime cannot see what a candidate touches.* `admit_layer_convening`
/ `admit_convening`
(`/home/brett/projects/xFactory/installs/hermes-install/src/hermes_install/domain/council_orchestration.py:451-478`)
receive exactly one candidate-derived input: `block`, from which they read
`block["council_id"]` and `block["subject_pin"]`. The runtime has no repository
access, no diff, no changed-path list, and never fetches the pin. To refuse "a
candidate that touches the machinery this council is assembled from," the
touched-object set must be **posted to it** — and the poster is
`.github/workflows/council-convening-lane.yml` in codexFactory, whose own header
comment concedes the tree-locality problem it is trying to solve ("the
base-branch checkout — not a pin — is what stops a candidate altering the rules
that govern it," `:36-45`). So the refusal code is outside the checked tree and
the refusal's **input** is authored inside it. A candidate that narrows what its
own commissioning lane reports as touched gets a clean admission. That is LS-A3
exactly: a control adopted on a description of an enforcement that does not
enforce it. Q6 asks what the refusal's *subject* is; nobody asks what its
*input* is or who supplies it, and that is the load-bearing question.

*(b) The content the refusal reads is not declared for codexFactory.* The
proposal cites
`contracts/hermes-domain-overlay/examples/hermes-domain-content-manifest.example.yaml:9`
for the `review_council → hermes/domain/review-councils` mapping. That is the
**example**. codexFactory's live manifest
(`/home/brett/projects/xFactory/xFactories/codexFactory/hermes/domain/content-manifest.yaml`,
unchanged since commit `135f761`) declares exactly one kind:

```yaml
content_set:
  domain_ontology:
    directory: hermes/domain/ontology
```

and the loader is explicit that a present manifest is exhaustive —
`load_domain_content_set`: *"An archive shipping
`hermes/domain/content-manifest.yaml` loads EXACTLY its declared set… an
undeclared kind never loads silently"* (`domain_content_set.py:176-186`). The
manifest's own comment ("other kinds remain on the documented convention until
this domain declares them") states the opposite of what the code does.
Consequence today: `domain_council_content` returns `(None, None, {})`, and
`admit_convening` refuses with `council.unseeded`. The mechanism §3 calls
"already provided" is, for the one domain this change is about, not reachable.

*(c) The floor's own source of truth is deliberately excluded from that
channel.* `add-substantive-review-lane/specs/roles-authority-model/spec.md:323-344`
makes the floor's SOURCE OF TRUTH codexFactory
`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`,
and says "where it and that record ever diverge the record governs."
`_find_dir_at` (`domain_content_set.py:83-95`) seeds only `*.yaml` and
hard-excludes `"/records/"`. So the authoritative text of the ceiling this
proposal declares untouchable is a markdown file that (i) lives in the reviewed
tree, (ii) is structurally excluded from the runtime that would enforce against
it, (iii) has no schema and no validator, and (iv) is gated only by `/hermes/
@brettheap` in CODEOWNERS — which `gh pr merge --admin` bypasses, and the
proposal's own motivating sentence is "Today every governed merge takes it." One
of the "three real controls" §3 enumerates is nullified by the practice the
change exists to end.

**Impact.** HIGH. The proposal's single retained structural property is
unenforceable as specified, and the specs phase would author a requirement
against a runtime that cannot satisfy it. Worst case: the intake ships, the lane
is wired, and a candidate touching council machinery convenes cleanly because
its own workflow under-reported its paths — with the audit trail showing a
governed, digest-provenanced convening.

**Suggestion.** Add to the `review-authority-intake` spec a requirement with
three limbs: (1) **the refusal's input is derived, never reported** — the
runtime SHALL compute the candidate's touched-object set from the subject pin's
own content or from an artifact the candidate's repository cannot author, and a
convening whose touched-object set is unavailable, self-reported, or
unverifiable SHALL be REFUSED rather than admitted; (2) name declaring
`review_council` (and `deliberation_mix`) in the target's
`hermes/domain/content-manifest.yaml` as a **stated precondition** in ## Impact,
with the note that a present manifest is exhaustive; (3) require the floor's
source-of-truth record to be moved into a seedable, schema-validated `.yaml`
carrier, or amend `roles-authority-model` so the promoted spec text governs and
the record is evidence — the current "the record governs" inversion puts the
constitution in an unseeded markdown file inside the reviewed tree.

---

## 2. Nothing bounds a root grant, no tool reads any grant, and the register's likely home is reviewed by its own grantees. HIGH

**Concern.** "Authority travels in grants" is sound only if minting a grant is
harder than asserting authority. Today it is strictly easier.

**Evidence.**
- `issued_by` is **optional** in
  `contracts/openxwallet/openxwallet-grant.schema.yaml:90` (not in `required:`,
  `:34-41`) and is read by **zero rules** in `scripts/validate-openxwallet.py` —
  I grepped the whole of `scripts/`; the only hits are unrelated
  (`hermes-job-envelope`, `doc_health` report headers). There is no notion of
  issuer authority anywhere in the contract family.
- Attenuation binds only where `parent_grant_ref` is present (`check_grant` rule
  (f), `validate-openxwallet.py:652-745`). A grant **without**
  `parent_grant_ref` is a root, and the only thing bounding it is the audience
  wallet's declared custody ceiling (see #3). Monotonic attenuation below an
  unbounded root is a strictly local property. Q2 poses "what bounds the issuer"
  and the proposal ships it unanswered while asserting the model in the present
  tense throughout.
- **The validator is not enforcement.** `.github/workflows/` in openxFactory
  contains exactly `doc-health-reusable.yml` and `session-open-pr.yml`;
  `validate-openxwallet` appears in neither, and there is no `tests/*wallet*`
  directory. Every rule the proposal leans on — the custody ceiling,
  attenuation, the audience binding, the revocation chain — runs only when a
  human types the command. This is precisely the CODEOWNERS precedent the
  proposal names in Q3 ("an authority declaration no tool reads is
  documentation") — and it is already true of the instrument it is composing,
  not just of the register it is proposing.
- **Circularity is not hypothetical, it is the favoured answer.** Q1's
  constraint (`canonical-policy-migration:33-38`,
  `repo-boundary-governance:8-13`) points the register at openxFactory.
  `add-substantive-review-lane` makes `opensoft/openxFactory` the **pilot
  repository** for the substantive review lane (`:149`). So the register that
  issues review authority would live in the repository whose PRs are reviewed by
  councils holding grants issued from that register. Nothing in the proposal
  declares the register a floored, human-only surface — a grant register is
  authority policy but is not literally "contract bytes, gate or workflow
  definitions, credential surfaces, or security posture," so it plausibly falls
  **outside** the floor's four clauses.
- **The anti-stand-in fixture does not reach the failure the intake creates.**
  `contracts/openxwallet/examples/negative/exercise-attributed-to-a-wallet-not-presenting-its-key.yaml:12-14`
  is an **exercise-record** rule: it works by deriving the presenting wallet from
  the verified proof key (`validate-openxwallet.py:840-880`). Q5 concedes "a
  council seat casting a GitHub review produces no wallet-signed exercise
  today," and offers exit B — record the grant, evidence the exercise by the
  existing council/enforcement audit trail. Under exit B **there is no exercise
  record**, so the fixture's key binding never runs. What is left is: an intake
  entry saying "seat X holds review authority over object Y," and an approval
  cast by the merge-master GitHub App — a shared installation credential, which
  `openxwallet/spec.md:93-111` says must be recorded as "transport, never as the
  actor," with the act recorded **`unattributed`**. A reader of the intake plus
  the check-run will attribute the act to seat X. That is the false audit record
  the fixture names, relocated one layer up from the record to the register. The
  proposal calls exit B "a declared deviation"; declaring it does not stop it
  being the thing.

**Impact.** HIGH. The instrument's forgery resistance is zero at the root and
its laundering resistance is zero under its own preferred exercise exit. A sole
operator writing a YAML file gives an agent `authority_tier: act` over any named
object, with no issuer check, no CI, and — if the register lands in the pilot
repo unfloored — clearance eligibility for changes to itself.

**Suggestion.** Three requirements, all cheap and all missing: (1) **`issued_by`
becomes REQUIRED, and a root grant is a named class** — a grant with no
`parent_grant_ref` SHALL name an issuer whose authority to issue is recorded
outside the register it writes into, and the specs phase names that anchor (Q2
must be *answered*, not carried). (2) **The intake register is itself a
permanently human-only surface under the constitutional floor**, declared
explicitly rather than left to inference from the four path clauses — otherwise
the councils clear their own commissions. (3) **No grant is operative until a
named validator reads it in CI**: state that an intake entry with no reader
confers nothing, and make wiring `validate-openxwallet` (or the register's
validator) into the target's required checks a precondition, not downstream
realization. On exit B: if it is taken, require the register to carry the
deviation *and* require the resulting audit record to be marked `unattributed`
per `openxwallet/spec.md:107-111` — do not let a recorded grant supply
attribution that no key established.

---

## 3. The custody ceiling is a self-declared string, and `act_unsupervised` is reachable in pure software. HIGH

**Concern.** §2's headline is "The ceiling is already structural — it is not a
new rule." It is not structural. It is one string in one YAML file, checked by a
script nothing runs.

**Evidence.**
- The full ceiling enforcement is `check_grant` rule (e): resolve
  `grant.audience.wallet_ref` → `wallet.custody.model` →
  `registry[model].authority_ceiling`, compare ranks
  (`validate-openxwallet.py:640-652`). The wallet's custody model is **declared
  by whoever writes the wallet record** (`openxwallet-record.schema.yaml:99-111`);
  `declared_by` is a free identifier with no attestation. `check_wallet_record`
  (`:613-627`) validates **only** that the model id is a member of the closed
  set. Nothing anywhere attests that a wallet declaring isolated custody actually
  has an isolated key. So "raising authority requires changing custody, not
  asserting trust" is realized as: raising authority requires editing one string.
- The registry's negative fixtures (`custody-registry-unearned-ceiling.yaml`,
  `custody-registry-readable-claims-holder.yaml`,
  `custody-registry-collapsed-ceilings.yaml`) test the **registry's internal
  derivation consistency** — that `evidences` follows from the two booleans. They
  cannot and do not test the wallet's declaration against reality. The proposal
  treats registry consistency as if it were deployment attestation.
- **The proposal's "both software models ceiling at `act`" is a claim about
  today's *choices*, not about software.** `isolated_per_use_authorized` reaches
  `act_unsupervised`
  (`contracts/openxwallet/openxwallet-custody.registry.yaml:81-94`), and its
  stated bar is "an authorization that context cannot itself supply — a hardware
  presence check, **an external policy approval, a separate custodian**."
  Neither of the last two is hardware and neither is required to be human. A
  remote signing service that requires an approval call from a second process
  satisfies the literal text: the key is isolated from the holder's execution
  context, and each use requires an authorization that context cannot supply. An
  AI reviewer configured that way declares `isolated_per_use_authorized`, and the
  validator hands it `act_unsupervised`. The proposal's own §2 quotes this clause
  and then reads it as if it said "hardware."
- The ceiling is checked **at static file-scan time and nowhere else**.
  `repo_scan` builds a context from the scanned repo's own records
  (`validate-openxwallet.py:1330-1385`) — a corpus "closed over itself." There is
  no exercise-time ceiling check because there is no exercise (Q5). So the
  ceiling binds a file, not an act.

**Impact.** HIGH. The proposal's strongest structural claim — "no delegated
agent discharges a terminal gate is a consequence of the custody registry, not a
rule this change adds" — is the load-bearing sentence for the whole safety
argument, and it rests on a self-report validated for spelling. If the specs
phase writes it as a consequence rather than a rule, the family ends up with a
stated ceiling and no mechanism, which is worse than an explicit rule because it
stops anyone looking.

**Suggestion.** Either (a) write the rule the proposal declines to write, scoped
so it is not a parallel vocabulary: "a grant conferring review authority SHALL
NOT name `authority_tier: act_unsupervised`, and the intake SHALL refuse to issue
one" — a scope restriction on one consuming capability is not a parallel
authority vocabulary and `openxwallet-agent-profile:65-69` does not bar it; or
(b) require the intake to record, per wallet, **what evidences the custody
declaration** (who verified the isolation, against what, when), and declare that
a custody model with no recorded attestation caps at `request` rather than `act`.
Also delete or qualify "today's software custody models both ceiling at `act`" —
name `isolated_per_use_authorized` and say explicitly whether a non-human
authorizer satisfies it. That sentence is currently the design's largest
unexamined assumption.

---

## 4. Revocation is specified against a runtime whose admission stamp is issuance-time by construction — and the strictest revocation rule feeds the `--admin` loop it exists to end. MEDIUM-HIGH

**Concern.** `openxwallet/spec.md:113-131` is emphatic: revocation is checked
**at exercise**, and "issuance-time validity is not accepted as evidence of
current validity." The runtime this change plans to consume is built the other
way, deliberately.

**Evidence.**
- `verdict_for_completion` (`council_orchestration.py:485-520`) takes the member
  roster **and** the content provenance from the `convening` stamp written at
  admission — the docstring says why: "the convening was authorized against that
  content." So a seat whose grant is revoked between commission and verdict is
  still a required member. Honoring the stamp is exactly the issuance-time trust
  `openxwallet:127-131` forbids. Dropping the seat trips
  `VerdictMissingSeatError` under `missing_required_seat: refused` (codexFactory
  `hermes/domain/review-councils/gate-rules.yaml`), so the convening parks. Q4
  poses the checkpoint ("convening admission, seat return, verdict consumption,
  or all three?") without noticing that the runtime's stamp semantics make "all
  three" a contradiction, not a menu option.
- Grant expiry has the same shape and no answer: `expires_at` is REQUIRED,
  `state` is a **field inside the grant record**, and nothing recomputes it. A
  grant that expires between commission and verdict is a record still reading
  `state: active`.
- **The composition rule is a live-fire hazard under a sole operator.**
  `openxwallet-agent-profile:27-48` revokes an agent's outstanding grants on
  **any** component change, "with no tolerance band and no grace period," and
  `distinctness_floor: composition_hash` makes model version a declared
  component. A provider silently rolling a model alias therefore revokes every
  seat grant in the fleet at once; with `missing_required_seat: refused`, every
  in-flight and future convening parks; the only routine exit from a parked
  candidate under a sole code owner is `--admin`. The proposal's motivating
  sentence is "A gate whose only habitual discharge is its own bypass is a
  ritual, not a control" — its own strictest inherited control manufactures
  exactly that condition.
- Propagation is asynchronous in the only register shape on the table. If the
  register is a file in a repo, "every grant derived from it is revoked **at the
  same moment**" (`openxwallet:121-125`) is unimplementable: revocation is a PR,
  review, merge. Nothing in the proposal names a revocation latency, a staleness
  bound, or a fail-closed default for "register unreachable or stale."

**Impact.** MEDIUM-HIGH. Not a security bypass — a liveness and coherence
failure that lands on the operator daily and trains the same bypass reflex the
change is written to break. The coherence half is worse: the specs phase would
write "revocation is checked at exercise" as a requirement of a capability whose
only runtime consumer is architecturally issuance-bound, producing a spec that
cannot be realized green.

**Suggestion.** Require the intake spec to (1) name the exercise checkpoint
**and** reconcile it with the admission stamp — the honest shape is a re-check
at verdict consumption that, on a revoked seat, parks with a named refusal
rather than silently honoring the stamp; (2) declare a revocation staleness
bound and the fail-closed behaviour when the register cannot be read at exercise
(unreadable register ⇒ refuse, never proceed); (3) address the
composition-revocation blast radius explicitly — either pin the model version as
a declared component and treat a provider roll as a planned re-issuance event
with a named runbook, or record why fleet-wide instant revocation is acceptable.
Do not leave it to be discovered by the first alias roll.

---

## 5. Digest-disjointness measures byte identity, which is not the axis the floor is about — and it is self-declared with unverifiable completeness. MEDIUM

**Concern.** The narrowed-floor option asks the bench to rule that a
digest-disjoint reviewer is not a member of the excluded class. The definition
offered is enforceable but it does not measure independence, and the corpus
already says so.

**Evidence.**
- **The corpus's own warning, in the schema the proposal is composing.**
  `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml:30-36`:
  *"Two agents from the same model, orchestrator and prompt are not independent
  the way two humans are; this constraint defends against slips and loops, not
  against a wrong policy applied consistently by both. The agent profile's
  composition hash gives an objective floor — different hash, different holder —
  and **whether that floor suffices is left to the consuming domain**."* The
  composition hash was shipped as a **distinctness** floor with an explicit
  disclaimer that it is not an independence test. The proposal repurposes it as
  an independence test to justify narrowing a floor whose stated target is
  correlated unanimity. That is using the primitive against its own recorded
  caveat.
- **It rejects the right case and admits the wrong one.** The proposal states
  plainly: "A different MODEL alone also fails: swapping weights under the same
  prompt contract and tool manifest changes one component of the declared set,
  not the set's intersection with *M*." So the case that most improves
  independence — different weights — fails prong (i). Meanwhile two seats on the
  same base model with independently authored prompts, tool manifests and corpora
  share **no** digests with *M* and pass cleanly, while being maximally
  correlated. The test is anti-correlated with the property it is proxying for.
- **Prong (i) is defeated by any re-derivation, and the proposal's fork claim is
  narrower than stated.** A fork fails only where bytes are identical. A fork
  whose prompts are regenerated from the same generator, or reformatted, or carry
  a version header, produces different digests and passes. "So do vendoring and
  copy-at-a-different-path" is true only for byte-identical copies — path is not
  part of a content digest, but a single changed line is.
- **The declaration's completeness is unverifiable.**
  `openxwallet-agent-profile:6-25` requires a hash over a **declared** set.
  `check_agent_composition` (`validate-openxwallet.py:1093-1158`) checks that
  content-bound components carry a digest and reference-bound components carry a
  ref plus a governing-configuration digest. It never checks a digest is
  *correct*, and it cannot check the set is *complete*. A reviewer can be
  digest-disjoint by omitting the components it shares with *M* from its
  declaration. Since the intake is where the declaration is recorded, and the
  intake would be written by the same operator who configures the reviewer,
  self-report is the whole chain.

**Impact.** MEDIUM — but it becomes HIGH the moment the bench rules for the
narrow reading, because that ruling is the only thing in this document that could
produce an autonomous approval on gate machinery. A wrong test here converts a
constitutional floor into a checkbox satisfiable by regenerating prompt files.

**Suggestion.** If the bench entertains the narrow reading, require the
definition to carry three additions: (1) **declared-set completeness is attested,
not assumed** — the reviewer's composition SHALL enumerate every component that
participates in its judgment, with the attestation recorded and the attester
named, and an incomplete or unattested declaration disqualifies; (2) **add a
base-model disjointness prong** — the excluded class is about correlated
judgment, so a reviewer sharing a base model with any seat of *M* is not disjoint
regardless of digests, which repairs the anti-correlation; (3) **carry the
schema's own caveat into the requirement text**, verbatim, so no future reader
mistakes the composition hash for an independence proof. Absent (1) and (2), the
honest recommendation is that the bench decline the narrow reading and the floor
stands — which is also the proposal's stated operative position everywhere else.

---

## What I could not break

The doctrinal reconciliations hold. "Authority never transfers"
(`doc-health:557-575`) really is scoped to the neutrality-drift lane, and
conferral-by-issuance really is a different act from conferral-by-discovery.
"Ownership confers no authority" (`client-infrastructure-liaison:18-30`) really
is conformed to rather than excepted, and the spec-authority / code-authority
rename is the right fix rather than a cosmetic one. The `consent-instrument`
non-precedent argument is correct on all three counts — the amendment-shape
incompatibility (`:115-126` vs `parent_grant_ref`) is decisive on its own.
Demoting the topology is right: `shared-contract-ownership:113-146` and
`adopt-neutral-tooling-home` would both have had to be overturned, and the
proposal is candid that the strongest evidence against its first spine became
evidence for its second. The refusal-only framing of the non-self-review rule is
genuinely safe — a rule that can only refuse cannot widen anything, and that
discipline is maintained consistently throughout.

The pattern in all five findings above is one thing: **the proposal repeatedly
treats a described control as an existing one.** It knows this failure mode by
name — it is built on LS-A3 — and it applies the lesson rigorously to
codexFactory's widen-only validator while granting the Hermes runtime, the
custody registry, and the composition hash the benefit of the doubt it denies the
mechanism it is replacing.
