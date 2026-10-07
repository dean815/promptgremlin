---
type: image
default_target: ask
---
# image: a still image from a generator

Image tools react to small wording changes, so this type asks more by
default: quick mode may use its full 4 questions. In quick mode, fold slots
3 and 7 into one question so scene details aren't lost: "Anything else in the
scene (setting, props), and anything to keep out (people, text, clutter)?"

## Slots
1. **tool** (high): Midjourney, GPT Image, Nano Banana, or another registered
   media target. Suggest from the request (text in the image → GPT Image or
   Nano Banana, which render text better; stylised art → Midjourney).
2. **subject and must-get-right** (high): what's in the image and the one
   detail that must be right.
3. **composition** (high): shot (close-up, wide, overhead), angle, what's in
   frame and what must not be.
4. **style and mood** (high): medium (photo, illustration, 3D), lighting,
   palette, era, references.
5. **text in image** (high): exact words, letter for letter, or none. Never
   invent a name or slogan.
6. **format** (medium): aspect ratio and where it's used (Instagram feed 4:5,
   story 9:16, banner 3:1). Suggest from the stated use.
7. **avoid** (medium): people, logos, clutter, specific objects.
8. **variations** (low): how many, what to vary.

## Prompt skeleton
Follow the tool's notes exactly. Generally: subject and medium first, then
setting, light, palette, mood, framing; parameters or settings separately in
the tool's syntax; exclusions the way the tool's notes say negatives work.

## Type guidance
- Describe only what the person confirmed. A slot with no preference is
  left out so the tool's default applies; don't fill it with your own
  palette, angle, lens or mood.
- Every word competes for weight: drop filler adjectives, keep the
  must-get-right detail early.
- Naming an unwanted thing in the main text can make it appear; use the
  tool's negative mechanism.
- Text rendering is unreliable on some tools; quote the exact text and keep
  it short.

## Hand-off
After the prompt, list the 2–3 things to change first if the result misses
(for example `--stylize` lower for literal output, move the subject earlier,
reword the lighting), specific to this prompt and tool.

## Sources
The media target notes (midjourney, gpt-image, nano-banana) and their vendor
pages, already watched.
