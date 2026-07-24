# Tasks — add-hermes-domain-content-manifest

- [x] 1.1 `contracts/hermes-domain-overlay/content-manifest.schema.yaml` +
      example (the codexFactory conventional set declared) + negative
      fixtures (unknown kind, ambiguous location).
- [x] 1.2 `contracts/memory-gateway/memory-binding.schema.yaml` + example
      (the two LIVE-derived opensoft bindings); provider/credential-surface
      prohibition enforced by the canonical validator.
- [x] 1.3 Validator extensions: `validate-hermes-domain-overlay.py` covers a
      present content manifest (self-test 10 fixtures + real codexFactory
      repo pass); `validate-memory-gateway.py` covers the binding shape,
      vocabulary cross-checks, and the no-provider-surface rule; both green.
- [x] 1.4 Contract release: manifest.yaml entry + CHANGELOG + contract-v1.18
      allocated (v1.17 verified current) + digest inventory built (179
      entries) + annotated tag published and verified.
- [x] 1.5 README doc-index (both contract-family READMEs) + OpenSpec Records
      block updated.
