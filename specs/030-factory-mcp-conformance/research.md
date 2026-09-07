# Research decisions

Status: draft
Kind: implementation

Decision: Draft 2020-12 JSON Schema; Python jsonschema plus an offline reference resolver and deterministic semantic passes. Synthetic fixtures exercise all three repetition modes. Codex mapping cites immutable source without shipping domain behavior.

Rationale: ratified design resolves scope; local code provides existing behavior. Use Draft202012Validator with contained offline resolution, fake clocks and synthetic dependencies. Alternatives rejected: live server, shared transport, universal payload, policy duplication and wall-clock sleeps. Operational adoption/cancellation remain deferred. No unresolved implementation research decisions.
