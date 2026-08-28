# Reserved-surface inspection: `qualify-avatar-live-voice` task 6.2.3

Status: record
Date: 2026-08-27 (local session date; 2026-08-28 UTC)
Inspector: Claude Opus 5 (agent), read-only against a fresh clone of
`opensoft/openxFactory` under a scratchpad, on branch
`change/avatar-consent-corpus` cut from `origin/main` at `22f15cdf` — the
first `main` carrying PR #451's §6.1/§6.3 wiring, which landed by REBASE
(merged commits `25d2ece0` + `d5b9ccf1`, so #451's own head sha `13f4e585` is
not an ancestor of `main` and never becomes one; the CONTENT is what
transferred, and the files this record cites are byte-identical across the
two). No file in any working checkout was read or written.

## What task 6.2.3 asks for, and what this record therefore is

> 6.2.3 CONFIRM UNTOUCHED, **by inspection rather than assertion**: the four
> reserved retention classes stay forbidden, `local_persistence` stays const
> false, and the frozen consent-purpose count stays 3.

"By inspection rather than assertion" is the whole instruction, and it rules
out the two easy discharges. It rules out writing "confirmed" in a task tick,
and it rules out adding a test and calling the test the confirmation — a test
proves the state at the moment it runs, whereas what 6.2.3 asks is whether
**this change touched these three surfaces**, which is a question about a
diff and is answered by looking.

So this is an INSPECTION: each of the three claims is walked to the file and
line that carries it, quoted, and checked against what this change actually
edited. Where a machine check for the same fact ALREADY EXISTS it is named —
because a reader is entitled to know the claim has a second, running guard —
and where one did not exist and was cheap, it was added and is named as
added. Neither of those is the deliverable. This record is.

## Scope of the diff this inspection is against

`change/avatar-consent-corpus` adds, and only adds:

- `contracts/avatar-client/synthetic-evaluation-corpus.yaml` (new)
- `contracts/avatar-client/canary-ephemeral-processing-envelope.yaml` (new)
- `tests/avatar_client_validator/test_section62_consent_corpus.py` (new)
- this record (new)
- `scripts/validate-avatar-client.py` — two new check functions, their
  constants, and two lines registering them in `run()`
- `contracts/avatar-client/README.md`, `README.md` — doc-index lines
- `openspec/changes/qualify-avatar-live-voice/tasks.md` — the §6.2 ticks and
  the amendment note

**It edits no schema, no registry, and no interface lock.** That is the
substance of the confirmation below; the walks make it checkable rather than
asking a reader to take it.

---

## Claim 1 — the four reserved retention classes stay forbidden

### 1a. The reserved set, at the registry

`contracts/avatar-client/registries/retention-classes.registry.yaml`, lines
13-17:

```yaml
13	reserved:
14	  - {id: full_transcript, description: "FORBIDDEN in this kernel; successor change only"}
15	  - {id: audio, description: "FORBIDDEN in this kernel; successor change only"}
16	  - {id: video, description: "FORBIDDEN in this kernel; successor change only"}
17	  - {id: independent_transcription, description: "FORBIDDEN in this kernel; successor change only"}
```

Four entries, each carrying its own "FORBIDDEN in this kernel; successor
change only". The file is **unmodified by this branch** — it is not in the
diff above.

### 1b. The active set that does NOT contain them, at the schema

`contracts/avatar-client/avc-07-retention-profile.schema.yaml`, lines 13-17:

```yaml
13	$defs:
14	  retention_class:
15	    type: string
16	    x-vocab: retention_class
17	    enum: [ephemeral_presentation, operational_telemetry, structured_record]
```

The enum is CLOSED to the three active classes. None of the four reserved
ids appears in it, so a retention profile naming one is structurally invalid
rather than merely discouraged. The schema description at lines 6-10 names
all four in prose ("Full transcript, audio, video, and independent
transcription are RESERVED and forbidden in this kernel"). **Unmodified by
this branch.**

The same closed set is mirrored a second time at
`contracts/avatar-client/shared-definitions.schema.yaml` lines 107-109
(`retention_marker`), also unmodified.

### 1c. The freeze pin

`contracts/avatar-client/interface-lock.yaml`, line 39, inside
`frozen.closed_defaults`:

```yaml
39	    reserved_retention_classes: forbidden
```

**Unmodified by this branch.** This change unreserves exactly `AVC-09` and
`AVC-10` — the two contract identifiers — and no retention class. The
identifier unreservation is the one at `interface-lock.yaml` lines 16-17
(`contracts:` now carrying AVC-09/AVC-10, `reserved_identifiers: [AVC-03,
AVC-05]`), and it is a different list on a different axis from the retention
freeze.

### 1d. The existing machine guards

- Registry-to-schema parity is compared SET-EQUAL:
  `scripts/validate-avatar-client.py` line 131,
  `"retention-classes": ("avc-07-retention-profile.schema.yaml", "retention_class")`
  inside `PARITY` (line 122). A reserved class moved into `members:` would
  fail parity against the closed enum.
- `contracts/avatar-client/fixtures/index.yaml` lines 276-284, case
  `avc07-reserved-class-refused`, drives `retention_class: full_transcript`
  and declares `expect: invalid` against scenario `ACR-010-S02`.
- `check_interface_lock` (`scripts/validate-avatar-client.py` line 3466)
  machine-compares the lock's frozen lists against the validator's own
  constants.

### 1e. One thing observed and recorded rather than smoothed over

`contracts/avatar-client/internal-live-activation-checklist.yaml` line 199,
inside condition 2's §7.9 `ruled_values.data_control`:

```yaml
199	        classes_never_instantiated: [audio, full_transcript, independent_transcription]
```

That list names **three**, not four; `video` is absent. The validator's own
comment says so plainly beside `CHECKLIST_S79_NEVER` in
`scripts/validate-avatar-client.py`: "The three the ruling says are never
instantiated in this ring. They are also three of the four RESERVED retention
classes". The list is compared SET-EQUAL at line 1165, so it may not be
widened by an editor either.

**This is not a defect and this inspection does not treat it as one.** The
§7.9 list is a narrower statement — the ring's canary-audio DATA CLASSES —
and `video` is absent from it because the ring has no video capability for it
to be a data class of. The RESERVATION of `video` is carried at 1a and 1b,
which is the level task 6.2.3 asks about, and it is intact. The promoted
requirement names all four, so the envelope this change adds names all four
in its own `never_instantiated` block and its check compares that block
against the REGISTRY's reserved set rather than against §7.9's narrower list —
the two lists are deliberately not merged, and neither is edited.

**Verdict: UNTOUCHED. The four reserved retention classes stay forbidden.**

---

## Claim 2 — `local_persistence` stays `const: false`

`contracts/avatar-client/avc-07-retention-profile.schema.yaml`, line 21:

```yaml
21	  local_persistence: {const: false, description: "No local persistence of sensitive session data"}
```

`const: false` — not `default: false`, not `enum: [false]`, not a required
field with a documented convention. A retention profile carrying
`local_persistence: true` fails schema validation; one omitting it is valid,
because the field is optional (`required:` at lines 22-23 names only
`retention_class`). **Unmodified by this branch.**

Exercised positively at `contracts/avatar-client/fixtures/index.yaml` line
275 (`local_persistence: false` inside `avc07-valid`, lines 266-275).

Nothing this change adds authors an AVC-07 instance. The envelope
(`canary-ephemeral-processing-envelope.yaml`) maps live-leg artifacts to the
two permitted CLASSES and cites the retention reference; it creates no
retention profile, so there is no place in this diff for a
`local_persistence` value to have been introduced at all.

**Verdict: UNTOUCHED. `local_persistence` stays `const: false`.**

---

## Claim 3 — the frozen consent-purpose count stays 3

### 3a. The registry

`contracts/avatar-client/registries/consent-purposes.registry.yaml`, lines
5-12:

```yaml
5	# Neutral consent-purpose registry — exactly the 3 ratified purposes (spec
6	# FR-005). Parity-checked set-equal against the shared-definitions
7	# `consent_purpose` enum. AVC carries only the consent record reference,
8	# version, and required purpose ids; domains own evidence/legal-basis/withdrawal.
9	members:
10	  - {id: avatar.media_capture, description: "Local microphone capture"}
11	  - {id: avatar.provider_processing, description: "Provider session creation/processing"}
12	  - {id: avatar.structured_record, description: "Retention of a structured workflow record"}
```

Three members. **Unmodified by this branch.**

### 3b. The schema mirror

`contracts/avatar-client/shared-definitions.schema.yaml`, lines 37-43:

```yaml
37	  consent_purpose:
38	    type: string
39	    x-vocab: consent_purpose
40	    enum:
41	      - avatar.media_capture
42	      - avatar.provider_processing
43	      - avatar.structured_record
```

**Unmodified by this branch.**

### 3c. The two independent count pins

- `contracts/avatar-client/interface-lock.yaml`, line 21, inside
  `frozen.registries`:

  ```yaml
  21	    consent-purposes: 3
  ```

- `scripts/validate-avatar-client.py`, line 133:

  ```python
  133	EXACT_COUNTS = {"session-result-reasons": 15, "consent-purposes": 3}
  ```

  enforced at line 412 with the `registry-count` finding.

Both **unmodified by this branch**; the validator edit in this diff adds two
functions and their constants below the §7.9 block and registers them in
`run()`, and touches neither `PARITY` (line 122) nor `EXACT_COUNTS`.

### 3d. What this change adds that could have moved the count, and did not

Task 6.2.2 admits an **optional stricter domain purpose REFERENCE**. A
reference is not a registry member: it resolves in the DomainxFactory's own
consent tree, and naming one adds nothing to the neutral registry. That is
why the ruling admits a reference rather than a fourth purpose, and the
envelope records it as
`optional_stricter_domain_purpose.does_not_change_count`. An
evaluation-specific purpose — the other way the count could have moved — is
refused outright (`consent.new_evaluation_purpose.admitted: false`,
scenario ALV-007-S03).

**Verdict: UNTOUCHED. The frozen consent-purpose count stays 3.**

---

## Belt-and-braces added by this branch (NOT the deliverable)

Task 6.2.3 says to add cheap validator assertions "if such checks don't
already exist". For claim 3's COUNT and claim 1's registry/schema PARITY they
already exist and are named above; nothing was added there, because a second
check of a checked fact is noise.

What did not exist is a guard on the two NEW artifacts re-stating these facts
wrongly, and that is where the additions went —
`check_ephemeral_processing_envelope` in
`scripts/validate-avatar-client.py`:

- the envelope's `frozen_purpose_count` is recomputed from the registry's own
  member list, so growing the registry makes the envelope's number wrong
  (proved by `test_the_purpose_count_is_read_from_the_registry`);
- the envelope's `never_instantiated.classes` is compared set-equal to the
  registry's `reserved:` ids — all four — so narrowing it, or unreserving a
  class in the registry, fails (proved by
  `test_narrowing_the_never_instantiated_list_is_caught` and
  `test_the_reserved_set_is_read_from_the_registry`);
- permitting a reserved class in the envelope fails
  (`test_permitting_a_reserved_retention_class_is_caught`).

Every negative in `tests/avatar_client_validator/test_section62_consent_corpus.py`
is a MUTATION OF THE REAL ARTIFACT in a tmp tree, on the shape
`test_section7_pinned_values.py` established, with a session-scoped teardown
asserting no shipped file was mutated.

---

## Result

| Claim | Surface inspected | Verdict |
| --- | --- | --- |
| Four reserved retention classes stay forbidden | `registries/retention-classes.registry.yaml:13-17`; `avc-07-retention-profile.schema.yaml:13-17`; `interface-lock.yaml:39` | UNTOUCHED |
| `local_persistence` stays `const: false` | `avc-07-retention-profile.schema.yaml:21` | UNTOUCHED |
| Frozen consent-purpose count stays 3 | `registries/consent-purposes.registry.yaml:9-12`; `shared-definitions.schema.yaml:37-43`; `interface-lock.yaml:21`; `scripts/validate-avatar-client.py:133` | UNTOUCHED |

All three confirmed **by inspection**. This change unreserves exactly AVC-09
and AVC-10 and no retention class, adds no consent purpose, and authors no
retention profile.
