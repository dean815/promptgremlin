# Effort suggestion

Rate the task on four signals, then pick the lowest level that clears the bar.
Higher effort costs time and tokens, so don't round up.

| Signal | Low | Medium | High | Max |
|---|---|---|---|---|
| Run length | one reply | a few steps | a multi-step session | a long autonomous run |
| Ambiguity | none | some, resolvable | real judgment calls | open-ended design |
| Verification | none | a glance | tests or checks | independent verification |
| Cost of a mistake | trivial | annoying | real rework | expensive or irreversible |

Choose the level where most signals land. One outlier signal moves the
choice up at most one level.

Use the control named in the target's Effort block, in that surface's own
words and scale. Map low / medium / high / max to the nearest level it offers.
If the surface has a picker but the notes name no levels, still give the
level (low / medium / high) and say "pick the nearest option", without
inventing option names. Write "not settable here" only when the surface has
no such control at all (a fixed-effort product).

Format: `Effort: <level> (<surface>: <exact control>). <one-clause reason>.`

A target that has an Effort block always gets a line, even when the block
names no levels (use the "pick the nearest option" form). No Effort block in the target's notes means no Effort line at all: write
nothing, not "Effort: none" or "not applicable". That holds for every prompt in
a split, including the media ones.
