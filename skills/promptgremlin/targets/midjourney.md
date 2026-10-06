---
family: midjourney
kind: tool
last_verified: 2026-10-01
sources: [prompt-basics, parameters, versions]
---
## All models
- Output one line: descriptive text first, then parameters. Every parameter goes after the last word of the description, never in the middle and never followed by more prose. (parameters#Using Parameters)
- Parameter syntax is exact: one space, then two dashes glued to the name, then one space and the value: `--ar 3:2`. No comma, period, or other punctuation after a parameter, and no stray space between the dashes. (parameters#Using Parameters)
- Keep the description short and plain; long instruction lists and chatty requests confuse it. Phrase it as a noun-led scene description, not a request to "show me". (prompt-basics#Prompting Tips & Tricks)
- Decide which of these matter to the user and name only those: subject, medium, environment, lighting, color, mood, composition. Whatever you leave out falls to the default house style, which gives more variety and less control. (prompt-basics#Prompt Length and Details)
- Order descriptors by importance: subject and medium first, then setting, light, color, mood, framing. The guide lists the categories but gives no ranking; this order is a convention. (hand-written)
- Pick precise words over generic ones, and exact counts or collective nouns over bare plurals. (prompt-basics#Choose the Right Words, #Be Specific with Numbers)
- Write what should be in the image. Naming an unwanted thing in the text can make it appear; exclusions go in `--no <word>` at the end instead. (prompt-basics#Focus on What You Want, parameters#Full Parameter List)
- Common parameters: `--ar` (aspect ratio), `--chaos` (variety), `--stylize` (artistic flair), `--raw` (less default styling), `--weird`, `--seed`, `--tile`, `--no`, `--v` (version). Short forms: `--c`, `--s`, `--w`, `--v`. (parameters#Full Parameter List)
- Reference images are not typed text. Image prompts, style references (`--sref`, strength `--sw`, `--sv` for its version), personalization (`--profile`), and the weight of an image prompt (`--iw`) attach by URL or upload in the interface; emit the parameter only when the user supplied the reference. (prompt-basics#Advanced Prompts, parameters#Full Parameter List)
- Video prompts use the same line plus `--motion low` or `--motion high`, `--loop`, `--end`, and `--bs` for batch size. (parameters#Full Parameter List)
- Add `--v <number>` only when the user needs a specific version; without it the current default (V8.2) runs. `--niji` switches to the anime-focused model line. (versions#Setting a Version, #Niji 7)

## v8-2
- Default version; set `--v 8.2` only to be explicit. Tuned for bolder, more edgy aesthetics and stronger use of the user's personalization profile. (versions#V8.2)
- Its Edit Model (`--edit`, written instructions plus up to four reference images) replaces Omni Reference, Character Reference, and the Retexture tool. Do not emit `--oref` here. (versions#V8.2, parameters#Full Parameter List)

## v8-1
- Use `--v 8.1`. Fast and reads small details well; add `--raw` to strip default styling when adherence matters most. (versions#V8.1)
- Introduced `--hd` (2048px output, aspect ratio capped at 4:1) and `--sd` (1024px). Use `--hd` only if the user wants higher resolution; it costs more GPU time. (versions#V8.1, parameters#Full Parameter List)
- Omni Reference is replaced by the Edit Model in V8.x, so no `--oref`. (parameters#Full Parameter List)

## v7
- Use `--v 7`. This is the version that introduced Draft Mode (`--draft`, half the GPU cost) and Omni Reference. (versions#V7, parameters#Full Parameter List)
- `--oref` works here for a person's likeness or an object's form, not on V8.x. (parameters#Full Parameter List)
