# Hermes-Layer Persona Character Model: how much personality should a decider have — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The open question spun out of the domain-content work: the Plane-1
Hermes authority personas (Lead Architect, Lead Security, Scrum Coordinator, …)
need *character* beyond a technical disposition — enough to make human
collaboration genuinely pleasant and to lift project quality — but personality
must never override deterministic governance. This doc frames what persona
"character" is for, the dimensions it spans, and a spectrum of options from
structured-disposition-only to a trait-framework-plus-authored-prose model,
with the load-bearing guardrail that character shapes *how* a persona decides
and communicates, never *whether* a gate holds. Sibling of
`codexfactory-domain-hermes-content.md`; grandchild of
`hermes-layer-content-seeding.md`.
Topics: hermes-persona, personality, character-model, authority-personas,
human-experience, trait-framework, persona-depth, behavioral-identity,
agent-certification, memory-gateway, client-tunability, domain-hermes
Repository context: openxFactory (applies to all Hermes-layer personas; piloted on codexFactory domain)
Captured: 2026-07-21

## Possible feats

- **Persona schema (neutral, openxFactory)** — the shape a Hermes-layer persona
  is authored in, whatever depth is chosen.
- **Trait-axis framework** — a small set of legible, tunable character axes.
- **Authored persona set for the codex domain deciders** — the flagship cast.
- **Persona guardrail contract** — the enforced separation of character from
  authority (character never changes a deterministic gate outcome).
- **Client-tunable persona surface** — the wizard-adjustable slice (voice,
  formality) over the domain-fixed core.

## The question

We want **full personalities** for the Hermes-layer personas — not just a
technical stance, but character that (a) makes human interaction interesting and
pleasant and (b) actually raises the quality of the work. The open question is
*how* to represent and bound that: how deep, along which dimensions, authored or
generated, fixed or evolving, and how to keep "pleasant" from eroding "governed."

There is no precedent to copy — no persona/system-frame text exists anywhere in
the repos today (the only "persona" artifact is the unrelated avatar-client UI
persona schema). So this is a genuine design choice, not a fill-in.

## What personality is *for* (four purposes, ranked by why we'd pay for depth)

1. **Functional judgment.** Disposition drives the discretionary part of a
   decision — a skeptical Lead Security weighs ambiguous evidence differently
   than a throughput-minded Lead Engineer. This is the part that already exists
   as implicit "disposition" and is non-negotiable.
2. **Quality lift.** A well-drawn reviewer catches more; a mentor-flavored
   coordinator raises the team's bar; deliberately *diverse* dispositions across
   the cast surface more (the same reason the review-lane runs multiple models).
   Character is a quality instrument, not just decoration.
3. **Human experience.** Collaboration with a coherent, warm, legible persona is
   pleasant and sustainable; a flat rules-engine voice is not. This is the
   explicit want.
4. **Trust / legibility.** A persona with a *predictable* character is one a
   human can anticipate and trust — you know how the Lead Architect will react
   before you ask. Predictability is itself a feature.

## The dimensions of character

A persona could be characterized along any of these; the options below differ in
how many they commit to and how they're expressed:

- **Technical disposition** — risk posture, review rigor, speed/quality bias. *(table stakes)*
- **Communication voice** — tone, formality, verbosity, use of humor.
- **Relational traits** — empathy, encouragement, patience, proactivity, how it
  delivers bad news.
- **Values / motivations** — what it optimizes for and what it always flags.
- **Relationship memory** — whether it remembers *this human* and prior context
  (ties directly to the ratified memory gateway and consent).
- **Identity stability** — whether the character holds across sessions and across
  the underlying model that happens to be running it.

## The load-bearing guardrail

**Character shapes *how*, never *whether*.** A warm, encouraging Lead Security
still fails a security gate closed; personality operates strictly *within* the
authority envelope and the deterministic gates — it colors tone, framing, and
judgment-within-discretion, and it must never soften, delay, or override a
gate verdict, an authority boundary, or a fail-closed default. This is the one
non-negotiable; every option below inherits it. "Pleasant" ≠ "permissive."

## The options

| Option | What a persona is | Human experience | Governance/consistency | Authoring cost |
| --- | --- | --- | --- | --- |
| **A — Disposition-only** | structured tags (rigor, risk, speed) | flat, functional | trivially deterministic | minimal |
| **B — Disposition + system-frame** | A + a written frame (stance + comm style) | warm, coherent voice | prose is harder to verify | moderate |
| **C — Full authored character** | a curated cast: voice, values, relational traits, light backstory | richest, most engaging | hardest to bound; drift risk | high, per role |
| **D — Trait-framework** | a vector over defined axes (rigor, warmth, verbosity, proactivity, humor…) | good, systematic | legible, comparable, **certifiable**, tunable | moderate; front-loaded |
| **E — Hybrid (lean)** | D as the spine + authored prose (B/C) for flagship roles + client-tunable surface | rich where it counts | framework-bounded, prose where warranted | moderate–high |

- **A** is safe but concedes the entire human-experience and quality-lift goal.
- **B** buys most of the experience for modest cost, but prose frames are hard to
  test/version and easy to let drift.
- **C** is the most delightful and the most dangerous: unbounded character is
  hard to keep from colliding with the guardrail, and expensive to keep
  consistent across a whole cast.
- **D** treats character as measurable data — which makes it *legible* (you can
  say how two personas differ), *client-tunable* (dial warmth up for one client),
  and *certifiable* (a persona is a point in trait-space with a behavioral
  battery — see below). Its risk is feeling mechanical if the axes are too few.
- **E** is the lean: a small neutral trait framework as the spine so personas are
  legible/tunable/certifiable, *plus* authored prose frames for the flagship
  deciders (Architect, Security, Quality) where voice matters most, *plus* a
  narrow client-tunable surface. Depth where it pays, bounds everywhere.

## Cross-cutting considerations

- **Client-tunability.** Some character should be a client-adjustable surface via
  the client-policy wizard (e.g. *voice/formality* — a buttoned-up client vs. a
  casual one), while the *core disposition* stays domain-fixed (a client cannot
  dial down Lead Security's rigor). Trait-framework options make this a clean
  split; prose-only options do not.
- **Behavioral identity / certification.** A persona expressed as measurable
  traits + a behavioral battery is a *quantified identity* — which lets us detect
  drift and version character deliberately (change beyond tolerance = a different,
  recertified persona). This connects directly to `agent-certification-wallets.md`.
- **Model-agnostic consistency.** Character lives in *content*, not in whichever
  model is running the persona today; it must hold across model swaps and across
  an MoA panel. A persona is a role the models *play*, not a model.
- **Cast coherence vs. diversity.** Do the personas share a house style (one
  coherent team) or deliberately contrast (diverse voices that catch more)? Likely
  a shared baseline of respect/clarity + deliberately varied dispositions.
- **Anthropomorphization / disclosure.** Pleasant character must not disguise that
  these are governed agents; a human should always be able to tell, and the
  persona should never leverage rapport to push past a gate.

## Decided (2026-07-21)

- **Option E** is the chosen model: a neutral trait-axis framework spine +
  authored prose for flagship domain deciders + a client-tunable voice surface,
  with the guardrail as a hard contract.
- **Cast coherence: no house style at the domain layer.** Each domain persona is
  defined independently — deliberately varied dispositions and voices (the
  quality-through-diversity argument). The coherent "house team" grouping is
  reserved for the **client/policy layer** personas, where one operating
  organization's agents should feel like a single team.
- **First build:** the codex domain roster is drafted in
  `codexfactory-domain-roster-draft.md`; Lead Security remains the guardrail
  stress test (warm in *how*, fail-closed in *what*).

## Open questions

- **Which trait axes**, and how many, before it feels either mechanical (too few)
  or unbounded (too many)?
- **Cast coherence vs. diversity** — shared house style, deliberate contrast, or
  a baseline-plus-variance model?
- **Client-tunable surface** — exactly which traits are client-adjustable (voice,
  formality?) and which are domain-locked (disposition, rigor)?
- **Relationship memory depth** — how much does a persona remember about a
  specific human, and under what consent (gateway `consent-profile`)?
- **Authoring authority** — who signs a persona into existence, and is a persona
  change a domain OpenSpec/ratification event (like the practice catalog)?
- **Evolving vs. fixed** — may a persona's character *grow* from experience, or is
  it versioned only by deliberate re-authoring? (Fixed is safer for trust;
  evolving is more human.)
