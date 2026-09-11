# Proposal Amendment: register-gate-rules-council-seats — Q-GRC-4 DISCHARGED for `client-security-compliance-officer`

Status: record
Kind: decision record
Decision date: 2026-09-11
Lane: hermes-wallet-exercise (window `codeXfactory-2`)
Ruler: Brett Heap (repository owner, operator), in session, window
`codeXfactory-2`, over the three top decisions the Q-GRC-4 discharge brief put
to him — who/what sits the seat and by which route, the exact model identifier,
and the vehicle (amend the open change or open a new one) — each presented with
the brief's recommendation first.
Ruled: 2026-09-11T14:59:26Z, verbatim: *"amend register-gate-rules-council-seats,
lead-architect route, same model pin as lead-security"*.
Ruling URL: NONE, and the absence is recorded rather than papered over — the
ruling was spoken in session and has no comment to cite. The precedent for an
in-session ruling carried by its record alone is this corpus's own
`split-opendox-two-layer-product/review/amendment-2026-09-05-repository-shape.md`,
whose `Ruler:` line likewise names a session rather than a URL. The immediately
adjacent standing ruling DOES have one and is cited below (cxF #279 comment
`5635898767`).
Amends: `register-gate-rules-council-seats`, RATIFIED 2026-09-06 (record
`review/ratification-2026-09-06.md`, Brett Heap, *"lets take them in your
recommended order all approved"* at 2026-09-06T14:13:46Z, ratified head
`169f84ef`), previously amended 2026-09-07 (R1/R2 — `lead-architect`'s pin and
the 5.9a re-sequence; carried as `proposal.md` § `## AMENDMENT — 2026-09-07`
and `design.md` § `## AMENDED 2026-09-07 — D3 sequencing`, with no review
record filed). **This is the packet's SECOND amendment.**
Read against: openxFactory `origin/main` `45bd9ee2`; codexFactory `origin/main`
`a990cba5`. Every line number below was re-measured at those two commits.

**THIS IS AN AMENDMENT, NOT A RE-RATIFICATION.** The packet stays ratified.
Q-GRC-4's ruling is not reopened and not contradicted: it said *"register
neither deferred seat NOW"* and named the trigger that would register one. This
amendment is that trigger arriving for ONE of the two — `intent_owner_role_slot`
stays deferred, untouched, on its own unchanged trigger. D1's four registered
seats, D2's one-body-one-row-no-per-seat-grant shape, D3's
composition-is-a-prerequisite finding, D4's mint-is-a-runbook decision, D5's
measured reader widening, D6's floor gap and D7's staleness bound all stand as
ratified. What this amendment adds is the SPECIFICATION of an act task 4.6
already owed and never described.

---

## 1. What Q-GRC-4 defers, and the exact spot a discharge writes into

**The open question, as proposed** (`proposal.md:307-321`), quoted:

> ### Q-GRC-4 — The two deferred seats
>
> `intent_owner_role_slot` is symbolic until the subject-layer roster lands.
> `client-security-compliance-officer` is named as a PERSONA on a conjunction
> pull-in, not as a seat id, and its predicate `rule_touches_security_posture`
> has an implementation and no caller.
>
> **Recommendation: register neither now; do not delete either.** Record both as
> owed registrations that trigger on a codexFactory roster act — the project
> roster binding for the first, a seat identifier for the second — and require
> that whichever act binds them registers the key in the same governed act, so
> the first convening that seats them is not the one that discovers a missing
> key.

**The ruling** (`review/ratification-2026-09-06.md:93-97`), quoted:

> - **Q-GRC-4 RULED — register neither deferred seat now; delete neither.**
>   `intent_owner_role_slot` and `client-security-compliance-officer` are
>   recorded as owed registrations that trigger on a codexFactory roster act,
>   which must register the key in the same governed act.

**The owed act** (`tasks.md:544-549`, task 4.6, still unticked), quoted in full:

> - [ ] 4.6 **[codexFactory]** When the subject-layer roster binds
>       `intent_owner_role_slot`, or when the roster gives
>       `client-security-compliance-officer` a seat identifier, register that
>       seat's key IN THE SAME GOVERNED ACT (Q-GRC-4), so the first convening
>       that seats it is not the one that discovers a missing key.

**The deferral as it stands in codexFactory today**
(`hermes/domain/review-councils/gate-rules.yaml:101-114` @ `a990cba5`),
quoted:

```
101:      - persona: client-security-compliance-officer
102:        layer: client
103:        declared_as: members.client.conjunction_pull_in.persona
104:        why: >-
105:          named as a conjunction PERSONA and not as a seat id. Its predicate
106:          `rule_touches_security_posture` is implemented, registered, and — since
107:          task 5.9a closed on 2026-09-07 — LOADED AND EVALUATED by the resolver.
108:          When it HOLDS and no seat identifier is declared the convening REFUSES
109:          with `conjunction_seat_unbound`; the seat is never dropped and no
110:          identifier is invented (CSC-C4: "I ask for no model and no default").
111:        composition: none
112:        registers_when: >-
113:          a codexFactory roster act gives this persona a seat identifier — the
114:          same governed act must register its key (Q-GRC-4)
```

**And the literal spot** (`gate-rules.yaml:152-161` @ `a990cba5`), quoted —
note that line 153 declares only `persona:`, and that there is **no `seat:` key
under `conjunction_pull_in` anywhere in the file**:

```
152:      conjunction_pull_in:                    # CSC/LS conjunction rule: a rule touching
153:        persona: client-security-compliance-officer
154:        when:                                 # security posture seats the CSC as a second
155:          predicate: rule_touches_security_posture   # client voice automatically
156:          params:
157:            security_surfaces:
158:              - "scripts/merge_master/**"     # the decision core
159:              - ".github/workflows/**"        # the gate definitions
160:              - "hermes/domain/review-councils/**"   # the councils themselves
161:              - "schemas/**"                  # contract bytes
```

**The executable consequence, not the prose one.** codexFactory
`scripts/merge_master/seat_resolution.py:566` reads `seat = pull_in.get("seat")`
and `:582` sets `"seat_identity": ("declared" if seat else "UNBOUND")`; `:583`'s
`unbound_why` is the sentence a refused convening returns, and `:691` is where
it surfaces as `unbound_conjunction_seats`. **That one `.get("seat")` is the
whole mechanical test a discharge has to satisfy**, and nothing else in the
resolver reads a second source for this persona's identity.

Measured live, not inferred: the C2 convening packet
(cxF `hermes/domain/review-councils/convening-packets/2026-09-11-routine-code-clearance-repository-respelling.md`,
merged to cxF main by PR
[#407](https://github.com/codeXfactory/codexFactory/pull/407) →
`76f2e77133c2c45eae3a6916b59ba6b3ac4a8cc2` at 2026-09-11T14:01:10Z) ran the real
builder against main and recorded `unbound_conjunction_seats` carrying this
persona, so a dispatch today **spends the subject pin and produces no sealed
request**.

---

## 2. The three rulings, verbatim, and what each settles

Brett Heap, in session, window `codeXfactory-2`, **2026-09-11T14:59:26Z**,
verbatim:

> **`amend register-gate-rules-council-seats, lead-architect route, same model pin as lead-security`**

Three rulings, and each answers one of the three questions put to him:

**RULING (1) — VEHICLE: amend this packet, do not open a new change.** The
brief's decision §4.8 asked amend-in-place vs. a sibling `amend-*` change. The
word is *"amend register-gate-rules-council-seats"*. This is the corpus's own
expectation restated as an instruction: the packet is still ACTIVE and
un-archived, its own task 4.6 names this exact act as owed to it, and its
directory is the holder's established walk-record home (task 3.9 — both
`walk-2026-09-08-register-act.md` and `walk-2026-09-11-register-act.md` live
there). **A sibling `amend-*` change was checked and is not available anyway**:
every archived `amend-*` precedent amends a PROMOTED capability under
`openspec/specs/`, and `review-authority-intake` is not promoted (§ 3 below
measures this), so such a packet would have no `specs/` target to write into.

**RULING (2) — ROUTE: the lead-architect route, not the tenant route.** The
brief's decision §4.3 was a real procedural question with no prior ruling: CSC
is declared under `members.client` like `company-policy-lead` (whose pin is a
TENANT `seat_representation` declaration, R23's inversion), but it is a
CONJUNCTION pull-in rather than an unconditional seat. The word settles it for
the DOMAIN route: codexFactory `hermes/domain/agent-mixes.yaml:709`,
`guardrails.roster_change: lead_accepted_recorded` — *"SEAT_MODELS /
model_assignments change = Lead Quality accepts + evidence record (never free
config, never ratification)"*. That route has **two halves, both required**:

- **the selection** — Brett's, given here; and
- **Lead Quality's acceptance**, produced by the `lead-quality` seat AT ITS OWN
  PIN (`claude-sonnet-5`) as an actual seat return. Precedent R1's acceptance is
  cxF `records/2026-09-07-seat-returns/lead-quality.md` (position "ACCEPT AS
  AMENDED", conditions LQ-C1..C4).

The evidence record takes R1's shape: cxF
`hermes/domain/review-councils/records/2026-09-07-gate-rules-roster-lead-architect-pin.md`,
whose § 0 / § 1 / § 2 / § 3 / § 5 / § 6 / § 7 headings this act's record
reproduces in their own places.

**What ruling (2) does NOT do, and this is the amendment's most easily-missed
consequence:** it does not make CSC a domain-layer persona. The persona stays
declared at `members.client` and its specialization stays the TENANT's
(`hermes/client/role-overrides.yaml:83-88`, the only text in the corpus saying
what CSC is for, quoted in § 4.1). What ruling (2) chooses is which AUTHORITY
ROUTE writes the model pin — and it chooses the recorded domain roster-change
act over a fresh tenant `seat_representation` declaration.

**RULING (3) — PIN: `claude-opus-5`, exactly `lead-security`'s.** The word is
*"same model pin as lead-security"*. Both `lead-security` blocks in codexFactory
`hermes/domain/agent-mixes.yaml` agree on the identifier, so the ruling is
unambiguous whichever the speaker meant:

| block | file:line @ `a990cba5` | `selector` |
| --- | --- | --- |
| `merge_readiness_council.model_assignments.lead-security` | `:56-61` | `claude-opus-5` |
| `gate_rules_council.model_assignments.lead-security` | `:329-339` | `claude-opus-5` |

**Q8(d) is not reopened**: an exact provider version, never a family. The pin
enters as `selector_kind: exact_provider_version`, `pin_status: pinned`.

**THE ONE FIELD THAT IS NOT COPIED, stated plainly because copying it would be
the natural mistake.** `gate_rules_council`'s `lead-security` block carries
`authority_ref:
hermes/domain/agent-mixes.yaml#review_council_profiles.merge_readiness_council.model_assignments.lead-security`
(`:338-339`) — it REFERENCES the enrolled roster because that seat's pin was
never re-selected for this body. CSC's was. Rulings (2) and (3) pull in
different directions on exactly this field and (2) wins it, because
`authority_ref` records WHO DECIDED, not WHAT WAS DECIDED: copying
`lead-security`'s would attribute CSC's pin to a merge-readiness roster act that
never made it. CSC's `authority_ref` therefore names its OWN record, in
`lead-architect`'s shape (`:327-328`). The spec delta's second requirement
states this as a general rule so the next seat pinned by equality does not have
to re-derive it.

**AND A PROPERTY THIS RULING ENDS, named rather than discovered later.** The
2:2 opus/sonnet split that the 2026-08-22 Q3 disposition sought and the
2026-09-07 R1 act explicitly preserved (`agent-mixes.yaml:331-333`: *"opus on
lead-architect and lead-security, sonnet on lead-quality and
company-policy-lead"*) becomes **3:2**. Any fifth seat ends it either way; this
records which way.

### 2.1 The standing ruling this discharge exists to lift

Brett Heap, **2026-09-11T14:23:26Z**, cxF #279 comment
[`5635898767`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5635898767),
verbatim: **`α, park C2 until Q-GRC-4 is discharged`** — option α of the 14:02Z
hold table, with β (a park-recording dispatch) and γ (a rule-reach re-cut) both
rejected, and **no subject pin spent**. C2 unparks when the seat is bound. The
two carried-forward words that then discharge are `convene C2`
(2026-09-11T13:26:14Z) and `merge the C2 record PR when green`
(2026-09-11T13:27:23Z). § 7 carries the dependency in full.

---

## 3. The form this amendment takes, and why — including one thing the tree REFUSES

**The form.** An IN-PLACE amendment of the active packet: this record, plus a
`## AMENDMENT — 2026-09-11` section in `proposal.md`, a
`## AMENDED 2026-09-11` section in `design.md`, a new `## 6` group in
`tasks.md`, three `## ADDED` requirements in the packet's own spec delta, and
the README OpenSpec Records row's amendment marker. Every edit is VISIBLE in the
tree, in the lifecycle's own inline form (`docs/document-lifecycle.md`), because
a ratified record whose text silently changed is a record nobody can cite. **No
ratified sentence is rewritten** — § 8 enumerates what does not move.

**`## MODIFIED Requirements` IS NOT AVAILABLE HERE, AND THAT IS MEASURED
RATHER THAN ASSERTED.** The discharge brief asked for the spec delta to be
`## MODIFIED`. It cannot be, for a reason the corpus has already written down
once, and two runs in this session confirm it:

1. **`review-authority-intake` is not promoted.** `openspec/specs/` carries 62
   promoted capabilities at `45bd9ee2` and this is not one of them: both changes
   authoring it (this packet and `amend-register-act-5b-projection-proof`,
   landed by openxFactory PR
   [#960](https://github.com/opensoft/openxFactory/pull/960) → `ac688c40`) are
   ACTIVE.
2. **The PATH CLI (1.2.0) refuses a MODIFIED block naming a requirement this
   same delta ADDs**, which is what an amendment restating its own ratified
   requirement would produce:
   `✗ [ERROR] review-authority-intake/spec.md: Requirement present in both
   MODIFIED and ADDED`.
3. **The PINNED CLI (1.12.0, the REQUIRED gate, run through
   `scripts/validate-openspec-cli-pin.py`) refuses a MODIFIED block with a FRESH
   title too — at archive time, which is worse**, because it validates
   `--strict` clean today and fails the day the packet archives:
   `ℹ [INFO] Archive would refuse this delta: review-authority-intake: target
   spec does not exist; only ADDED requirements are allowed for new specs.
   MODIFIED and RENAMED operations require an existing spec.`

The corpus already says this in its own words about a sibling packet, in this
repository's README: *"a `## MODIFIED` block would target text that is not yet
canon"*. **So the delta is `## ADDED`, appended to the block this packet already
owns** — three new requirements, taking it from 7 to 10. The README row's
*"**7 ADDED requirements** … no `## MODIFIED` and no `## REMOVED`"* sentence
moves with it.

**And the requirement this amendment DISCHARGES is not restated.** The packet's
ratified fourth requirement — *"A symbolic seat and a conditionally pulled-in
persona are not registered until the council seats them by identifier"* —
already carries the scenario this act exercises:

> #### Scenario: A conditional seat carries an identifier
> - **WHEN** a council's roster seats a conditional seat by identifier
> - **THEN** its key is minted and recorded with the unconditional seats, so
>   that the first convening the condition holds for is not the convening that
>   discovers a missing key

That requirement is not amended, narrowed or reopened. **This act is that
scenario being run**, and the three ADDED requirements state what the run itself
proved was unstated: what a convening does while the seat is unbound, how a
by-equality pin is attributed, and what must be true of the register before the
grant is re-issued over the widened composition.

---

## 4. THE ACT — HALF 1 (H1): the codexFactory roster act

**Owner: the lane, built via Speckit AFTER this amendment is ratified.** Nothing
in H1 is authored by this pull request; codexFactory is not touched by it. What
follows is the SPECIFICATION, at the grain a builder can execute and a reviewer
can refuse.

**The seat identifier is `client-security-compliance-officer`** — the persona
string itself. This is an AUTHORING DECISION, not a ruling, and it is flagged
for veto in the same form `.openspec.yaml` uses for this packet's other
authoring decisions. It rests on three things and nothing else: the identity
`company-policy-lead` already holds between its persona and its `seat:` key
(`gate-rules.yaml:131`); the register's `seat_id` grammar, which admits it
unchanged; and `seat_resolution.py:566`, which requires only a non-empty string
and forces no relation to the persona. A different identifier would work
mechanically and would make the secret name, the wallet `display_label` and the
`deferred_seats` pointer all read against the persona they describe.

### 4.1 `gate-rules.yaml` — the binding itself

- **ADD `seat: client-security-compliance-officer`** beside `persona:` under
  `members.client.conjunction_pull_in` (`:152-161`). This is the edit that turns
  `seat_resolution.py:582`'s `"seat_identity"` from `UNBOUND` to `declared`.
- **EDIT the `deferred_seats` entry at `:101-114`** — do not silently delete it.
  Its own text says why (`:92-93`: *"so a reader comparing the roster with the
  composition does not read it as an omission"*). It becomes a DISCHARGED entry
  pointing at the record, or moves to a `discharged_seats` sibling; either way
  `intent_owner_role_slot` (`:115-126`) stays exactly as it is, on its own
  unchanged trigger.
- The raw material for the seat's charge is the TENANT's own declaration, and it
  is the only text in the corpus describing what CSC is for
  (`hermes/client/role-overrides.yaml:83-88`), quoted:

  ```yaml
    - persona: client-security-compliance-officer
      specialization: >-
        The company frame over an engineering estate: repo access, CI secrets,
        supply-chain exposure. The conjunction rule pairs this seat with the
        domain's Lead Security — both verdicts independently on any risk that
        is both company- and engineering-shaped.
  ```

  **No `seat_representation` block is added there.** Ruling (2) chose the domain
  route; adding one would perform a second, unruled tenant act.

### 4.2 `agent-mixes.yaml` — the declared composition

Four edits inside `review_council_profiles.gate_rules_council`, all at
`a990cba5` line numbers:

1. **`all_possible_seats` (`:271-275`)** gains the identifier — a five-element
   list. The profile's own comment at `:251-270` (which names Q-GRC-4 and says
   *"Adding a seat to THIS list without that act would declare a composition for
   a seat with no wallet key"*) is rewritten to record the discharge rather than
   the deferral.

2. **`model_assignments` (`:312-372`)** gains the seat's entry. **The pin block,
   field by field, with the source of each field named** — `selector`,
   `selector_kind` and `pin_status` are `lead-security`'s (`:334-336`) verbatim
   under ruling (3); `authority_layer` is `lead-architect`'s route value
   (`:326`), which is the same token `lead-security` carries; `authority_ref` is
   NOT copied, per § 2 ruling (3)'s last paragraph:

   ```yaml
         client-security-compliance-officer:
           selector: claude-opus-5                     # = lead-security (:334), RULING (3)
           selector_kind: exact_provider_version       # = lead-security (:335)
           pin_status: pinned                          # = lead-security (:336)
           authority_layer: domain                     # the lead-architect ROUTE, RULING (2)
           authority_ref: >-
             hermes/domain/review-councils/records/<date>-gate-rules-roster-csc-pin.md#operator-ruling-<id>
   ```

   The `authority_ref` shape is `lead-architect`'s (`:327-328`), pointing at H1's
   own record anchor rather than at another seat's block.

3. **`prompt_contract.seats` (`:378-382`)** gains the identifier, and **the
   seat's briefing has to be WRITTEN — there is nothing to copy.** The briefing
   is not a file: it is a per-seat constant in
   `.github/workflows/scripts/deliberation_packet.py`,
   `GATE_RULES_SEAT_FOCUS` (`:225-258`), rendered by `seat_system_prompt`
   (`:1546`) and reachable as
   `python3 .github/workflows/scripts/deliberation_packet.py seat-prompt
   --council-id gate_rules_council --seat <seat>`; the sitting-artifact
   convention for the rendered text is
   `records/<date>-<sitting>-artifacts/seat-prompts/`. The existing four were
   *"WRITTEN FROM THE RECORDS, NOT FROM THE SEAT NAMES … drawn from what this
   body's own convenings actually charged it with"* (`agent-mixes.yaml:390-394`).
   **CSC has never sat and no convening has ever charged it**, so that method is
   unavailable and the ONLY raw material is § 4.1's tenant specialization. The
   builder writes it from that, and says in the comment that it did.

4. **The digest re-pin (`:445-467`)**, which is what makes 1-3 a DECLARED
   COMPOSITION CHANGE rather than an edit:
   - `rendered_set_digest` (`:447`, today
     `sha256:aac9b60e877d5ab61324ebb5102fe24b685b1bcc1d97aecf9f6c8ef254358f21`)
     moves, recomputed by `digest_basis` (`:453-459`): sha256 over the UTF-8
     concatenation, **for each seat in LEXICOGRAPHIC order of the seat name**, of
     `<seat> NUL <rendered prompt> NUL`.
   - `seat_digests` (`:463-467`) gains a fifth entry. Because the ordering is
     lexicographic, `client-security-compliance-officer` sorts **FIRST** of the
     five (`cli` < `com` < `lea`), so the new prompt enters at the head of the
     concatenation and every byte after it shifts — the digest cannot be
     patched, only recomputed.
   - `pinned_on` advances and `previously_pinned_on` takes `"2026-09-10"`.
   - The declaration is held equal to the LIVE RENDER, never to a typed value
     (`:383-388`, precedent `016e9f43`): `test_gate_rules_holder_composition.py`
     re-renders all five and proves the digest matches, and the digest coupling
     is proved BOTH ways — edit-without-repin fails, edit-with-repin passes —
     exactly as cxF PR #374 did.

### 4.3 The record, and the acceptance

A `roster_change: lead_accepted_recorded` record in R1's shape, at
`hermes/domain/review-councils/records/<date>-gate-rules-roster-csc-pin.md`,
carrying R1's own sections in their own places: § 0 what this record is and is
not (no seat was convened; the selection is Brett's); § 1 why a ruling was asked
for rather than a value authored; § 2 the ruling as given, verbatim, with its
UTC; § 3 the roster this record fixes (all five seats, and the 2:2 → 3:2 split
recorded); § 5 what this record does NOT claim (**no comparative claim: no soak
has run on this body's bench and none has run on this seat**); § 6 Lead
Quality's acceptance — **OWED, at `claude-sonnet-5`, as an actual seat return**,
with the OWED slot stated if it has not yet been produced; § 7 the soak re-opens
(C13, `soak_gate`'s `seat_roster_fixed_and_recorded_before_first_soak_row`:
*"a soak run on roster A cannot license activation on roster B"*), which **costs
nothing today for the same reason it cost nothing at R1** — no gate-rules
convening has ever run a seat through the deliberation lane and no soak row
exists (`agent-mixes.yaml:299-305`).

**LQ-C4's `tool_manifest` bound carries onto this seat unchanged**: this
council declares no tools, no workspace and no browser for any seat, and whether
a packet-only seat can meet its charge without running anything remains
untested. That applies to CSC exactly as it does to the other four, and the
record says so rather than letting a new seat imply new capability.

### 4.4 The mint (operator)

One Ed25519 keypair, `holder_readable` custody — **Q-GRC-1's ruling of
2026-09-06T14:13:46Z already covers this key and was never scoped to four
seats**. Private half generated in-process and passed to `gh secret set` on
stdin with `--body` omitted, stored ONLY as a GitHub Actions secret in
codexFactory's `worker-credentials` environment under the GRC-NAMESPACED name
`COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`. The
namespacing is not cosmetic for the other four (three of their names collide
with merge-readiness's own secrets); for CSC there is no collision, and the
namespace is kept anyway so one body's secrets are one prefix. A codexFactory
mint record mirrors
`records/2026-09-08-gate-rules-seat-signing-keys-minted.md` and publishes the
PUBLIC half, the `did:key:`, and the fingerprint — never the seed. **Who
performs this is OQ-1** (§ 9).

---

## 5. THE ACT — HALF 2 (H2): the openxFactory register act

**Owner: Brett Heap, as operator.** `governance/review-authority/register.yaml`
is a permanently human-only surface by ratified requirement and a
never-clearable floor member by exact path in codexFactory's gate rules. No
agent writes any file in this section. It is specified here as a WALK, exactly
as `tasks.md` § 3 specifies its own.

**The trigger is automatic and unconditional.** `docs/governed-reissuance-runbook.md`
§ 0.1 quotes the ratified rule: any change in an agent's declared composition
ends that agent's certified identity, and *"the change alone is sufficient to
revoke, AND no threshold, score, or tolerance band is consulted."* Both
`model_assignments` and `prompt_contract` are `content`-bound declared
components of this holder's composition, so **H1 landing revokes `grant-grc-0002`
at that instant**. There is no route that avoids this and none is sought.

**Five writes, one commit** — four are the runbook § 5.1 atomic acts as this
lane performed them on 2026-09-11 (`walk-2026-09-11-register-act.md` § 5), and
the fifth is the one the precedent did not have:

1. **REVOKE** `governance/review-authority/grants/grant-grc-0002.yaml` in place:
   `state: active` → `revoked`, plus `revocation.revoked_at` (one instant) and
   `revocation.reason` naming the composition event. Class **DRIFT** — the only
   class this corpus names, and *"any single component change is sufficient"*
   makes the class not a real choice; the free-text sentence names SEAT ADDITION
   rather than the precedent's prompt-corpus pin move.
2. **MINT** `grants/grant-grc-0003.yaml` — new `grant_id`, `state: active`,
   `issued_at` equal to the revocation instant, `issued_by` the ratifying human,
   `expires_at` per **OQ-2** (§ 9), scope re-examined rather than copied, and
   **no `parent_grant_ref`**: a superseding grant is a ROOT grant, not a derived
   one. The shape is `grant-grc-0002.yaml`'s.
3. **REPOINT** `register.yaml`'s `row-grc-0001` (`:182-190`): `grant_ref` →
   `grant-grc-0003` and nothing else. `expires_at` moves only if the new grant's
   differs; `state` stays `active`; **no second row** — D2's single-row-per-body
   shape is unchanged, and a seat is not a holder.
4. **ADD the fifth `seat_keys` entry** to `register.yaml`, after
   `company-policy-lead` (`:358-364`), in the four-field-plus-three shape the
   block already uses (`:333-339`):

   ```yaml
     - seat_id: client-security-compliance-officer
       council_ref: agent:gate-rules-council
       council_id: gate_rules_council
       key_id: key-grc-seat-client-security-compliance-officer-0001
       public_key: <43 chars, canonical unpadded base64url, VERBATIM from the mint record>
       key_fingerprint: sha256:<64 hex, RECOMPUTED by the reader from public_key>
       authorizing_row: row-grc-0001
   ```

   `council_ref` must equal the authorizing row's `holder_ref`; the reader's
   own checks (exact seven-name field set, fingerprint recomputation, uniqueness
   of `seat_id`/`key_id`/`key_fingerprint`, `authorizing_row` resolving to an
   ACTIVE unexpired row) all run inside the REQUIRED `wallet-validation` check.
   **No private half, seed or passphrase may ever appear in this file** — a
   64-hex seed pasted here is refused by shape before it can merge.

5. **ADD the fifth key to the wallet**, `wallets/wal-agent-grc-0001.yaml`'s
   `keys:` array, in the entry shape at `:125-135`:

   ```yaml
     - did: "did:key:z<multibase>"
       key_id: key-grc-seat-client-security-compliance-officer-0001
       key_fingerprint: sha256:<same 64 hex as the register entry, byte-identical>
       public_key_multibase: z<multibase>
       signature_algorithm: ed25519
       display_label: gate rules council — client-security-compliance-officer seat
       custody:
         model: holder_readable
         registry_version: 1
         declared_at: "<the mint instant>"
         declared_by: Brett.Heap
   ```

   `did` and `public_key_multibase` are DERIVED from the mint record's public
   half through the PINNED decoders (`scripts/validate-factory-identity.py
   --derive`), never by a second tool. **Both places are required, not one**: the
   register knowing a key is not the wallet declaring it, and the pinned
   validator's rule (r) refuses a presenting key no wallet declares — without
   this entry the first CSC seat return would be refused on arrival.

   The file's own comment block (`:114-124`) currently says CSC and
   `intent_owner_role_slot` are *"DELIBERATELY ABSENT under Q-GRC-4"* and will be
   added *"by whichever codexFactory roster act binds them, in that same
   governed act."* **That paragraph is this act's own instruction and it must be
   edited to record the discharge**, leaving `intent_owner_role_slot` named as
   still absent.

6. **ONE WALK RECORD**, at
   `openspec/changes/register-gate-rules-council-seats/walk-<T2-date>-register-act.md`
   — the holder's established home (task 3.9), beside the 09-08 and 09-11 walks.
   It carries R8's five minimum fields (superseding grant ref, superseded grant
   ref, the composition hash it was issued against, the ratifying human, the
   effective time), the runbook § 0.3 three-capacity disclosure, and — because
   R6/R7 remain PENDING — the composition recorded as declaring-commit plus
   digests, by the 2026-09-11 walk's own method rather than a hash the estate
   does not yet compute.

**The consuming gate's literal counts move in the same act.** `code_surface`
already names `.github/workflows/openxwallet-consumer-gate.yml`'s positive
assertions as moving with a registration, *"because a wildcard there would let a
register that lost a body pass the positive proof."* This act takes the
gate-rules half from four keys to five; the assertion that names the count moves
with it, in H2's own commit.

---

## 6. THE CEREMONY — the order, and what each step actually proves

All of it has been exercised once already, in full, by this lane
(`walk-2026-09-11-register-act.md`). What is new is step 0's mint and step 3's
fifth key; everything else is the same walk.

| # | step | actor | what it proves |
| --- | --- | --- | --- |
| 0 | Mint the fifth keypair; provision the secret; write the cxF mint record | OPERATOR | the key exists before anything declares it |
| 1 | **HOLD posted** on the tracking issue, the PR and `LANES.md` **BEFORE** the H1 merge | lane | the park is declared, not discovered (precedent cxF #374: hold posted 2026-09-10T23:20:38Z, ~14 min ahead of its own merge) |
| 2 | **T1** — H1 merges | Brett's word | `grant-grc-0002` is void FROM THAT INSTANT; `gate_rules_council` convenings park |
| 3 | **T2** — H2 merges (§ 5's five writes + walk record) | OPERATOR | the widened composition is certified again |
| 4 | **3.8 window check** — no `gate_rules_council` convening ran between T1 and T2 | lane | nothing convened against a void grant. Method: `gh run list --workflow gate-rules-convening-trigger.yml` cross-checked against `records/` commits in the window, as walk § 13.1 did ("empty under both candidate upper bounds") |
| 5 | **5b — the register-projection source-revision read** | **OPERATOR WORD REQUIRED, not self-serve** | the published projection has caught up |
| 6 | **HOLD LIFTED**, citing T2's merge commit and the walk-record path | lane | the park closes on evidence, not on elapsed time |
| 7 | **`resolved-seats` re-run** against a security-surface-touching subject | lane | `unbound_conjunction_seats` is now **EMPTY** — the concrete verification this whole act exists for |
| 8 | **Proof convening** on a re-verified clean candidate | Brett dispatches | five seats resolve, admitted and sealed (precedent: the 2026-09-11 walk § 15, run `34586762846`, admitted). **Whether this is a separate convening or IS C2 is OQ-5** |
| 9 | **C2** — dispatch the packet at `76f2e771` with a freshly re-selected clean candidate | Brett dispatches | the carried-forward words discharge; § 7 |

**Step 5 is the one that changed since the runbook was written, and this
amendment inherits the correction rather than repeating the error.** An ADMITTED
CONVENING PROVES NOTHING about the register projection: the convening-admission
path reads the DOMAIN-CONTENT projection only, while the REGISTER projection
carrying grant state is read inside `verdict_for_completion`, which this
council's lane never reaches. The walk record's own words: *"A green validator
does not lift the hold. An ADMITTED convening does[, was the runbook's claim,
and] it does not hold."* The PROVEN substitute is an operator-word-gated,
read-only cluster read of the `hermes-register-projection` ConfigMap confirming
its `hermes.opensoft.one/source-revision` annotation is at or after T2's merge
sha (walk § 14.1), on Brett's explicit word each time (precedent, verbatim:
*"Operator word: hermes-wallet-exercise reads it"*, 2026-09-11T03:01:28Z).

**This is now RATIFIED, not merely dispositioned, and the correction is
cited rather than re-derived.** `amend-register-act-5b-projection-proof`
(openxFactory PR [#960](https://github.com/opensoft/openxFactory/pull/960) →
`ac688c40`, merged 2026-09-11T14:16:46Z; ratified on Brett Heap's word
*"accept all A on 960"* at 2026-09-11T13:09:12Z and encoded at `5daa96ec`) makes
the direct observation of the published projection's declared source revision
the exit condition, in four ADDED requirements on this same capability. **The
discharge brief this amendment was written from states that change was not
filed. It was — that is the brief's one error, and it is corrected here.** Step
5 above is #960's requirement, not a lane improvisation, and the walk record's
`## Disposition — design § D4 step 5b` citation should be re-pointed at #960 at
the parents' archive cycle.

---

## 7. The C2 dependency, and the three words it discharges

C2 is the routine-code-clearance convening for the repository respelling. Its
packet is ON codexFactory main — PR
[#407](https://github.com/codeXfactory/codexFactory/pull/407) →
`76f2e77133c2c45eae3a6916b59ba6b3ac4a8cc2`, merged 2026-09-11T14:01:10Z — and
its dispatch is HELD, with **no pin spent**, because its subject is under
`scripts/merge_master/**`, one of the four `security_surfaces`
(`gate-rules.yaml:158`). The conjunction therefore HOLDS on C2, the CSC seat is
UNBOUND, and a dispatch would park after the claim job spends the subject pin
and would produce no sealed request.

Brett's standing word is § 2.1's `α, park C2 until Q-GRC-4 is discharged`
(2026-09-11T14:23:26Z). **C2 unparks when this act completes — not when this
amendment is ratified.** Ratification authorizes the build; step 7 of § 6's
ceremony (`unbound_conjunction_seats` empty) is what actually lifts α.

Two words are then carried forward and discharge in one motion, both Brett's,
both still standing:

- **`convene C2`** — 2026-09-11T13:26:14Z (as *"merge the packet PR when green
  then convene C2"*; the packet half is already discharged by #407's merge).
- **`merge the C2 record PR when green`** — 2026-09-11T13:27:23Z.

**C2 will be the first convening in this estate at which the conjunction fires
with a bound seat**, so its record is where `rule_touches_security_posture`
finally has a caller AND a seat, which is the state
`gate-rules.yaml:142-149` records as missing today.

---

## 8. What this amendment does NOT move

- **Q-GRC-4 is not reopened and not contradicted.** It ruled *"register neither
  deferred seat NOW"* and named the trigger. This is the trigger, for one seat.
- **`intent_owner_role_slot` stays deferred**, byte-identical, at
  `gate-rules.yaml:115-126` and in `wal-agent-grc-0001.yaml`'s comment. Its
  trigger — the subject-layer roster binding — has not arrived and nothing here
  brings it closer.
- **D1 through D7 are unchanged**, including D2's one-body-one-row shape: this
  act adds a fifth SEAT KEY, never a second authority row, and a seat is not a
  holder.
- **Q-GRC-1, Q-GRC-2, Q-GRC-3 and Q-GRC-5 are not reopened.** Q-GRC-1's
  `holder_readable` determination covers the fifth key without a second ruling
  (it was never scoped to four). Q-GRC-3's date is OQ-2's default rather than a
  reopening. Q8(d) — exact model versions only — stands.
- **No promoted requirement is authored, modified or removed.**
  `openspec/specs/` is not touched by this pull request.
- **No codexFactory file is edited by this pull request.** H1 is SPECIFIED here
  and BUILT after ratification, through Speckit, in its own repository.
- **No register, wallet, grant or attestation byte moves here.** H2 is Brett's
  operator act; this pull request writes governance prose and a spec delta only.
- **No box is ticked.** § 6's new group lands entirely open, including its own.
- **No corpus-ledger row is seeded.** `register-gate-rules-council-seats`
  already holds one (`tests/sequenced_after/corpus-ledger.yaml:260`,
  `state: active`, `class: sole`, `moved_by: "#717"`), and an amendment moves no
  state; `--ledger-diff` re-proves this on the final tree. This differs from
  #960, which was a NEW change and therefore had to seed one through the
  sanctioned tool.
- **`sequenced_after:` does not move.** It still reads
  `[add-wallet-carried-review-authority,
  openXwallet:widen-register-reader-for-a-second-council]`; this amendment
  declares no new upstream.
- **The `Ratified:` and `Lane:` header lines are untouched** — the split-opendox
  precedent's rule, applied here: a record's header states the act that made it,
  and an amendment adds a line rather than rewriting one.
- **The archive gate (§ 5.1-5.3) is not widened.** § 4 of `tasks.md` is
  EXPLICITLY out of the archive gate by its own § 5.2, and task 4.6 lives in
  § 4. § 6 inherits that: **this discharge does not become a new archive
  condition**, and § 6.9 says so on its own row. What DOES change is § 5.3's
  re-read, which will now find five seats rather than four.

---

## 9. Open questions this amendment does NOT decide

Five, each with lettered options and one RECOMMENDED from precedent. Every
recommendation is what the text above already encodes, so **taking all five
recommendations moves no byte of this packet.**

**OQ-1 — Who mints and holds the fifth keypair?**
- **(a) RECOMMENDED — Brett Heap, host-side, the task 3.2 ceremony generalized
  to one seat.** The four existing keys were *"MINTED BY THE OPERATOR (Brett
  Heap) with a lane-authored, HOST-SIDE program that is in NO repository"*, seeds
  generated in-process and never written to disk, passed to `gh secret set` on
  stdin with `--body` omitted. Custody `holder_readable`; secret name
  `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`; record in
  `records/2026-09-08-gate-rules-seat-signing-keys-minted.md`'s shape. It is a
  fresh TTY-gated ceremony, not a rerun of stored state.
- (b) Mint through the repository-committed `scripts/mint-factory-origin-key.py`
  instead — that script is the ORIGIN-key ceremony, and D4 already decided the
  seat mint is a runbook rather than a script.
- (c) A different custody model for this key alone — would break the uniform
  `holder_readable` posture Q-GRC-1 ruled for this body and give one seat a key
  the holder job cannot read.

**OQ-2 — `expires_at` on `grant-grc-0003`?**
- **(a) RECOMMENDED — `2027-06-30T00:00:00Z`, unchanged.** Q-GRC-3's reason —
  one re-issuance ceremony covers both bodies and the two grants cannot silently
  diverge — is untouched by a fifth seat, and `grant-mrc-0002` still carries that
  date.
- (b) Recompute from the earliest published retirement floor among the five
  pinned identifiers, by the 2026-09-11 walk's own method. **Today this returns
  the same date**, because the fifth pin IS `claude-opus-5`, already on the
  bench — so (b) differs from (a) only in showing its working.
- (c) A shorter expiry for the new seat — refused by shape: the grant is
  addressed to the WALLET and the row carries one expiry; there is no per-seat
  expiry to set.

**OQ-3 — Does the CSC briefing need a soak, or an `activation_gate` pass,
before the seat sits live?**
- **(a) RECOMMENDED — bind now, soak later. The lead-architect precedent
  exactly.** R1 bound the pin; LQ-C1's four-class integration soak (≈$3, ≥6
  candidate judgments) was commissioned AFTER and is still open under a
  LANE-DEFECT-FIRST disposition. C13 re-opens this body's soak from zero and
  **costs nothing today**, because no gate-rules convening has ever run a seat
  through the deliberation lane and no soak row exists.
- (b) Require an LQ-C1-shaped fresh soak at the CSC pin before the seat may
  sit — parks C2 behind a soak that has never gated any seat of this body, and
  inverts the order R1 set 4 days ago.
- (c) Declare a `gate_rules_council` `activation_gate` of its own. **Measured:
  none exists.** `activation_gate` is the ENROLLED merge-readiness surface's key
  (`scripts/merge_master/codexfactory-routine-code-clearance.yaml` and
  siblings); neither `gate-rules.yaml` nor this profile declares one. (c) is new
  machinery, not a gate being honoured.

**OQ-4 — One PR pair in the T1/T2 shape, or split further?**
- **(a) RECOMMENDED — the T1/T2 PAIR: one codexFactory PR (H1), then one
  openxFactory PR (H2).** Two pull requests because there are two remotes; ONE
  governed act because the hold spans them. This is the shape the 2026-09-11
  re-issuance used end to end (cxF #374 → oxF #941).
- (b) Split further — mint record, roster act, composition re-pin as separate
  codexFactory PRs. Re-introduces exactly the window Q-GRC-4's *"same governed
  act"* rule exists to close: a roster that names a seat whose key is not yet
  registered.
- (c) One single cross-repository act — not available; two remotes cannot share
  a commit.

**OQ-5 — Does C2 double as the seat's first live (proof) convening?**
- **(a) RECOMMENDED — a SEPARATE proof convening precedes C2**, on a re-verified
  clean candidate, exactly as the 2026-09-11 walk did (§ 15, run
  `34586762846`, admitted). C2's subject is under `scripts/merge_master/**`, so
  C2 is the convening the CONJUNCTION FIRES on; proving the five-seat bench on
  the same dispatch that first exercises the conjunction conflates two proofs,
  and a failure would not say which one failed.
- (b) C2 IS the proof convening — one dispatch, five seats, and both
  carried-forward words discharge in one motion. Cheaper by one pin, and the
  read-only `resolved-seats` run (ceremony step 7) already proves the binding
  without spending anything.
- (c) Two proof convenings, one non-security-surface and one security-surface,
  before C2 — the most evidence and the most pins; nothing in the corpus asks
  for it.

**One authoring decision, flagged for veto rather than asked as an OQ**
(the form `.openspec.yaml` uses for this packet's other authoring decisions):
the seat identifier string is `client-security-compliance-officer` (§ 4, first
paragraph).

---

## 10. What changed, file by file

| file | before | after |
| --- | --- | --- |
| `proposal.md` header | `Ratified:` + `Lane:` + `Family:` | a new `Amended: 2026-09-11` line naming the three rulings, the UTC and this record. `Status:`, `Ratified:`, `Lane:` and `Family:` UNTOUCHED |
| `proposal.md` § AMENDMENT | one section, `## AMENDMENT — 2026-09-07` | that section byte-identical, plus `## AMENDMENT — 2026-09-11 (Q-GRC-4 discharged for the CSC seat)` after it |
| `proposal.md` § Q-GRC-4 (`:307-321`) | the ratified question and recommendation | the same text, byte-identical, followed by a `> Amended 2026-09-11.` note recording that the trigger arrived for one of the two seats and pointing at this record. **The ratified paragraphs do not move** |
| `design.md` header | `Lane:` + the seven-decisions sentence | unchanged |
| `design.md` § AMENDED | one section, `## AMENDED 2026-09-07 — D3 sequencing` | that section byte-identical, plus `## AMENDED 2026-09-11 — Q-GRC-4 discharge (D8-D12)` appended at the end of the file, carrying five decisions mapped 1:1 onto OQ-1..OQ-5. **D1-D7 are not rewritten** |
| `specs/review-authority-intake/spec.md` | 7 `## ADDED` requirements, 21 scenarios | 10 `## ADDED` requirements, 30 scenarios — three appended to the same block. **No `## MODIFIED`, no `## REMOVED`** (§ 3 measures why) |
| `tasks.md` | §§ 1-5, last line 571 | the same, plus `## 6. Q-GRC-4 discharge (AMENDMENT 2026-09-11)` — H1, H2, ceremony, C2 unpark, and the archive-gate non-widening. **Nothing is ticked, including in §§ 1-5** |
| `README.md` OpenSpec Records row | `(R1/R2 amendment 2026-09-07)`; *"**7 ADDED requirements** … no `## MODIFIED`"* | both markers updated — the amendment marker gains this one, and the count reads 10 with the measured reason `## MODIFIED` is unavailable. **No other row moves** |
| `review/amendment-2026-09-11-q-grc-4-discharge.md` | — | this file |

**Six files plus this record.** Every one is inside the change's own directory
except the README row, which the split-opendox amendment precedent's own form
requires (*"the change's OpenSpec Records row"*). Nothing under `governance/`,
`contracts/`, `docs/`, `scripts/`, `.github/` or `openspec/specs/` is touched,
and **no file in any other repository is touched at all**.

---

## 11. Verification, from this session's own runs

Every command below was run from the worktree root
(`~/projects/xFactory/openxFactory-worktrees/amend-q-grc-4`) against the final
tree, and each against a throwaway baseline worktree at `origin/main`
`45bd9ee2` for comparison. The table lives in the pull request body, where a
reviewer reads it; the commands are:

- `OPENSPEC_TELEMETRY=0 openspec validate register-gate-rules-council-seats --strict`
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the failure set must
  be BYTE-IDENTICAL to the baseline's two
  (`disposition-codexfactory-declared-renames`,
  `disposition-codexfactory-floor-relocation-retitle`)
- `python3 scripts/validate-openspec-cli-pin.py --all` — the pinned 1.12.0
  entrypoint, the only route this repository permits, and the one that reports
  the archive-time refusal § 3 measures
- `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`
- `python3 scripts/doc-health.py --single-repo . --fail-on error`, diffed
  against the same run on the baseline

Structural checks carried in the pull request body: SHALL on the FIRST body line
of all three new requirements (the strict parser reads only that line); at least
one `#### Scenario:` per requirement; `design.md`'s D8-D12 mapping 1:1 onto
OQ-1..OQ-5; `Lane: hermes-wallet-exercise` on every document this amendment
touches.
