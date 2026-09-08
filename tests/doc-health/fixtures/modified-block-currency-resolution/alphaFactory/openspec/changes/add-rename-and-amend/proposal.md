---
code_surface: none
target_release: none
Status: ratified
---

# Proposal: add-rename-and-amend


Renames a promoted requirement and modifies it in ONE delta. Without
own-rename-first resolution the family would report every rename-and-amend
change as unresolved, and would compare nothing where it should compare
everything.

