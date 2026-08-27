---
code_surface: none
target_release: none
Status: ratified
---

# Proposal: add-li-b

This proposal names exactly ONE change id, and it is a LONGER one that merely
begins with its sibling's: `add-li-a-extended`. It declares nothing about the
sibling, because a change id occurring inside a longer one satisfies nothing —
the whole-token match the duplicate packet family already uses.

NOTE FOR WHOEVER EDITS THIS FIXTURE: do not write the sibling's bare id anywhere
in this file, not even while explaining what the fixture is for. The first cut
of this file did exactly that in its own prose and the fixture silently began
testing the opposite case, reporting a declaration where it meant to report
none.
