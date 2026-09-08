# add-zz-first

Status: ratified

## Why

This change modifies a requirement that the active ratified change
add-aa-second already modifies, and declares its deltas relative to that
change's outcome, exactly as `release-realization`'s "Ordered deltas and branch
vocabulary" requires. That declaration IS the ordering: this change is the LATER
writer.

Note the ids. `add-zz-first` sorts LAST alphabetically and `add-aa-second`
sorts FIRST, deliberately, so that name-ascending ordering picks the WRONG
writer. Do not "tidy" these names into agreement with the declaration — the
disagreement is the whole point of the fixture.
