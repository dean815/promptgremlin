---
type: video
default_target: ask
---
# video: a clip from a video generator

In quick mode, fold setting and exclusions into one question: "Anything
else in the scene, and anything to keep out?"

## Slots
1. **tool** (high): Veo, Runway, Kling, Sora, Higgsfield, or another media
   target. Suggest from the request (audio needed → a tool with native audio).
2. **subject and action** (high): what's on screen and what happens.
3. **camera** (high): shot size and movement (static, slow push-in, orbit,
   handheld).
4. **duration and format** (high): seconds and aspect ratio, from where it's used.
5. **style and light** (medium): look, lighting, palette, references.
6. **start or end frame** (medium): an image to start from, or none.
7. **audio** (medium): none, ambient, dialogue (exact words), music.
8. **avoid** (low): things to keep out.

## Prompt skeleton
Follow the tool's notes: usually subject and action, then camera, setting,
light and style, then audio; settings in the tool's syntax.

## Type guidance
- Describe only what the person confirmed; slots with no preference are
  left to the tool's default.
- One clear action per clip; several actions in a few seconds blur.
- Name camera movement explicitly; unstated, tools pick their own.
- Dialogue in quotes, short.

## Hand-off
List the 2–3 things to change first if the clip misses, for this tool.

## Sources
Video target notes (google-video, runway, kling, sora, higgsfield).
