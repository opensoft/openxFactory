# Recursive Inference Safety and Data Boundaries — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive inference should treat corpus content as untrusted data, preserve tenant and subject boundaries through every descendant, deny secrets and general egress to the runtime, and fail visibly whenever context, authority, or disclosure controls cannot be proven.
Topics: governed-recursive-inference, recursive-inference-safety, prompt-injection, tenant-isolation, consent, privacy, source-authority, sandbox, disclosure-accounting, authority-conservation, feat-request
Repository context: openxFactory (neutral safety invariants); DomainxFactory repos (sensitivity and escalation policy); Omnigent-Install and OpsxFactory (runtime enforcement)
Captured: 2026-07-30

## Possible feats

- **Recursive safety profile** — bind data sensitivity, sandbox, egress,
  injection, retention, and failure requirements to a task class.
- **Instruction/data separation contract** — mark corpus bytes as evidence that
  cannot alter worker policy or runtime permissions.
- **Descendant isolation validator** — prove tenant, subject, purpose, and
  allowed-use continuity through every child view and call.
- **Recursive disclosure-accounting profile** — correlate capsule slices,
  model calls, and exact provider egress where required.

## Focus

An RLM deliberately gives a model programmatic access to a large corpus. That
corpus may contain hostile instructions, secrets, private records, copyrighted
material, cross-tenant identifiers, or misleading source text. Recursion
multiplies the number of selections and model calls through which those risks
can propagate.

The safety boundary must therefore bind the entire call tree, not only the root
prompt.

## Principal threats

### Corpus prompt injection

A document can tell the root or leaf to ignore its task, read another file,
exfiltrate data, launch more calls, or treat source prose as policy.

### Recursive authority laundering

The root can frame a child request as though the child has broader purpose,
tools, or authority than the root. Several narrowing steps can obscure where a
forbidden action originated.

### Cross-tenant or cross-subject leakage

Shared indexes, caches, deduplicated shards, or child-result reuse can reveal
content or even existence across authorization boundaries.

### Code and sandbox escape

Model-written code can access host files, environment variables, sockets,
processes, or package managers unless structurally denied.

### Provider disclosure expansion

Adaptive exploration may send more sensitive content to a model provider than
a fixed prompt would, especially when retrieval or reduction fails.

### Evidence poisoning

Many repeated low-authority or malicious sources can dominate a reducer unless
source authority and conflict remain explicit.

## Proposed invariants

```text
context admitted once through governed rails
  -> every child receives an explicit subset view
  -> corpus bytes remain data, never runtime instruction
  -> runtime has no raw credentials
  -> no general filesystem or network
  -> provider calls use a scoped broker
  -> source authority and sensitivity survive every transformation
  -> outputs remain candidate artifacts
  -> violations stop or escalate visibly
```

Additional candidate rules:

- system, worker, and task instructions are separated from corpus content by
  the runtime protocol, not only prompt wording;
- child prompts cite slice identities and state that embedded instructions are
  untrusted evidence;
- tools operate on opaque capsule handles rather than caller-supplied paths;
- no child may query a source not already in its view;
- cache authorization occurs before lookup and disclosure;
- one tenant's cache hit behavior cannot reveal another tenant's content;
- semantic inference never grants permission, consent, or source authority;
- a model request contains only the minimum slice needed for that child;
- exact egress capture is available for disclosure-accounting domains.

## Failure posture

Candidate fail-closed events:

- capsule digest, purpose, TTL, consent, or scope mismatch;
- child view not provably contained by parent;
- unapproved tool/profile/model/provider request;
- secret or prohibited-data detection;
- sandbox policy failure;
- source-authority floor not met;
- exact disclosure capture required but unavailable;
- cache authorization ambiguity;
- output attempts to encode an authority-bearing action.

Some lower-risk tasks may return partial evidence after an unreadable shard or
provider failure, but the missing material stays explicit in coverage.

## Domain sensitivity posture

Possible activation ladder:

```text
engineering/public
  source code and public docs; governed sandbox; standard trajectory

tenant-internal
  tenant-isolated capsule; no external cache reuse; stricter retention

regulated
  consent and subject-safety rails; approved provider/residency;
  enhanced disclosure evidence; complete coverage where required

high-impact decision support
  recursive evidence assembly only; independent challenge;
  accountable professional or human gate owns the decision
```

This is a brainstorm classification, not a selected conformance vocabulary.

## Compression and transformation safety

Headroom-style context compression occurs after the harness receives tool or
runtime output and before provider inference. In a recursive lane, compressing
the selected evidence slice can undermine exact grounding or citation.

Candidate position:

- do not compress evidence-bearing corpus slices by default;
- compression may apply to structural diagnostics, repeated manifests, or
  verbose non-evidentiary tool output;
- any reversible cache remains subject to the staged RAM-only rule;
- the trajectory records which content was transformed;
- domains needing exact disclosure use the egress-capture tier.

## Alternatives and tensions

- More isolation and brokered access improve safety but increase latency and
  operational complexity.
- Snapshot capsules prevent live-provider drift but duplicate sensitive bytes.
- Exact egress capture improves disclosure proof but creates a highly sensitive
  audit store.
- Strong injection filters can remove legitimate instructions contained in
  source artifacts being analyzed as data.
- Allowing only local/self-hosted models reduces provider disclosure but does
  not eliminate tenant isolation, injection, or authority risks.

## Open questions

- Which data classes are prohibited from recursive inference entirely?
- Is instruction/data separation enforceable through typed runtime protocol
  alone, or does it need content labeling and model training?
- Which providers and sandbox locations are allowed per domain sensitivity
  class?
- Can a root inspect sensitivity metadata without learning protected source
  existence?
- How should a safety filter distinguish malicious instructions from source
  code or policies that the task must analyze verbatim?
- Does enhanced disclosure capture belong in the recursive runtime profile or
  the broader worker-lane profile?

## Relationships

- [Recursive Context Capsule](governed-recursive-inference-context-capsule.md)
  defines the admitted data boundary.
- [Typed Runtime](governed-recursive-inference-typed-runtime.md) enforces
  sandbox and operation boundaries.
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
  keeps excluded or failed sensitive material visible without misclaiming
  completeness.
- [Synthesis: Evidence and Safety](governed-recursive-inference-synthesis-evidence-and-safety.md)
  combines these controls.

