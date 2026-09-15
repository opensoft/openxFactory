# Targets That Resolve

Status: draft

<!-- xspec:candidate target=widget -->
the in-tree form, unchanged by the pinned arm
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:named-capability/wallet-carve -->
PRESENT AND NAMES: the pin record enumerates this capability
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:tree-digest/tree-capability -->
shape (b): one digest over the whole tree, neither per-file list
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:published-artifact/published-capability -->
shape (c): no dispositions:, which is absent-is-empty at the guard
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:no-path-only/host-resolved-capability -->
shape (a): no pinned_by_commit_only:, which the guards default empty
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:openxwallet/openxwallet -->
verify_pin: carries the value the adapter holds for this pin id
<!-- /xspec:candidate -->
