# ARC_BASE for each repository (T003)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T003
([`tasks.md`](../tasks.md)) · **Taken**: 2026-09-25, 13:34–14:02Z ·
**Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`).

## What the bases are for

5.4a's and 12.5's falsifiers find the arc's landings in a repository with this
command:

    git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD"

- The range `$ARC_BASE..HEAD` leaves ARC_BASE itself out.
- The guards read only commits that carry the trailer.

So any `main` commit from before the arc's first landing in a repository will
serve as its base. Each base below is that repository's `main` at the time T003
ran, and none of the seven holds an arc landing yet.

The two spec legs get a base even though no task lands in them yet. If T009
selects T053, openDox-spec joins the arc. Under R1Q12 (b), openXdox-spec joins
too. Their bases are then already recorded.

## The bases

| repository | ARC_BASE (its `main` at 13:34:54Z) | subject |
|---|---|---|
| `opensoft/openDox-code` | `1e4a57fb3c550339e25bb2fcc8da8e3a7817650f` | Name the sixth stage's short word as it is declared: completed (#36) |
| `opensoft/openXdox-code` | `e28930bf052febff0c7bdd0463a72ce3c4f5e8fe` | Resolve the snapshot validator and its schemas in this product's own tree (split-opendox § 8.9 residue (i)-(iii)) (#28) |
| `opensoft/openDox` | `36ded1cd97ca8f23b0eb9ea03d1d9def79a40d3c` | openDox contract changelog: Status draft → standard, the tag now exists (RULED item 3) (#12) |
| `opensoft/openXdox` | `069fe471f2ef5d23ea4461c0e0abd9f2768b6a31` | openXdox root: bump code to e28930bf (openXdox-code #28, the snapshot validator's § 8.9 residue) (#19) |
| `opensoft/openxFactory` | `c415c3d16663a8b17da5ae4f5e599f0971bf552f` | Plan 034: the Speckit plan for release 1 (standalone operation) of add-neutral-product-standalone-operability (#1155) |
| `opensoft/openDox-spec` | `8fe8c4c71c4da8d363394441ad9e2c9547e540a3` | Carry the surviving -v2 chat-turn family into openDox — the forward half of retire-doxbench-chat-turn-v1, and only that (§ 6.2) (#15) |
| `opensoft/openXdox-spec` | `f088b09732e236279898b53ab9fb0f5ebc89509a` | Receive add-nightly-dashboard-refresh: the refresh lane, re-homed under RULING Q6 (§ 6.1) (#15) |

openXdox-code's base already contains C3's PR 2 (openXdox-code#28, landed as
`e28930bf`), and openXdox's base already contains C3's root bump. Neither
landing carries the trailer, so neither ever counts as an arc landing.

## How each base was checked

The `main` of every repository was read at 13:34:54Z and read again at
14:02:10Z, with the same seven answers:

    for r in openDox-code openXdox-code openDox openXdox openxFactory openDox-spec openXdox-spec; do
      git ls-remote "https://github.com/opensoft/$r" refs/heads/main
    done

Each repository was then cloned at that commit, and the trailer was searched
for. The first count takes the guards' first-parent line, and the second takes
all of the history:

    git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' HEAD | wc -l
    git log --format=%H --grep='^Arc: neutral-product-standalone-operability$' HEAD | wc -l

| repository | first-parent | all history |
|---|---|---|
| openDox-code | 0 | 0 |
| openXdox-code | 0 | 0 |
| openDox | 0 | 0 |
| openXdox | 0 | 0 |
| openxFactory | 0 | 0 |
| openDox-spec | 0 | 0 |
| openXdox-spec | 0 | 0 |

A looser search, `git log -i --grep='Arc:'`, finds eight commits across five
of the seven repositories. None of them is a trailer:

- openDox-code `0f1f2e59` and `da8aae96`, openXdox-code `5da58ee2` and `208656fb`,
  openDox-spec `1a216ea4` and openXdox-spec `481a07f9` all quote the older
  BUILD-arc ruling ("BUILD arc: start now…") in prose.
- openxFactory `c415c3d1` and `94b6f7f1` say that bookkeeping carries no
  `Arc:` trailer, or that 11.0 adds one.

## PACKET_MERGE, for openxFactory's guard (11.1)

`PACKET_MERGE` is `94b6f7f13b45c351b9142345738965c974b7dd37`, "File
add-neutral-product-standalone-operability: open the BUILD arc, recording ten
rulings (#1144)". It is #1144's own landing on `main`. Its one parent is
`f1c690b8` (#1148), and it lies on openxFactory `main`'s first-parent line:

    git rev-list --first-parent HEAD | grep -c '^94b6f7f13b45c351b9142345738965c974b7dd37$'   # 1

F11.1 reads the arc's openxFactory landings as `$PACKET_MERGE..$ARC_TIP`, not
from ARC_BASE (#1144 `tasks.md`, 11.1's falsifier). openxFactory's ARC_BASE is
recorded above only because T003 names all seven repositories. Nine commits
lie between the two on the first-parent line, and none of them carries the
trailer.
