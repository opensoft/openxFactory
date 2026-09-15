# Lexically Malformed Pinned Values

Status: draft

<!-- xspec:candidate target=pinned:one/two/three -->
an extra segment
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:../x/y -->
a traversal component
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:Upper/case -->
an upper-case component
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:x/ -->
an empty component
<!-- /xspec:candidate -->

<!-- xspec:candidate target=pinned:dotted.name/x -->
a dotted component
<!-- /xspec:candidate -->
