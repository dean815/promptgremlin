---
family: sora
kind: tool
last_verified: 2026-10-01
sources: [prompting-guide]
---
## All models
- Some things are API parameters, not prose: `model`, `size` ("1280x720"), `seconds` ("4", "8", "12", "16", "20"; default "4"), `characters`. "Make it longer" in the prompt does nothing; output them as a settings line apart from the prompt. (prompting-guide#API Parameters)
- Shorter clips follow instructions more faithfully. Prefer two 4-second shots stitched in editing over one 8-second clip when the project allows. (prompting-guide#Video Length)
- Write the shot as a storyboard frame: prose scene, then camera framing and angle, depth of field, lighting and palette, then actions as beats. (prompting-guide#Prompt anatomy that works, #Prompt Structure)
- One camera move and one subject action per shot. Break the action into countable beats and say which beat lands at the end of the clip, so timing is concrete. Keep several shots as separate blocks, each with its own camera, action, and lighting. (prompting-guide#Control motion and timing, #Prompt anatomy that works)
- Set the overall look first (era, film stock, or genre), then layer details. Replace vague adjectives with things the camera can see and actions it can follow; list three to five palette colors. (prompting-guide#Visual cues that steer the look, #Lighting and color consistency)
- Short prompts leave Sora room to improvise; long ones give control but are followed less reliably. Anything unspecified gets invented, so pick the level on purpose. (prompting-guide#Prompt anatomy that works)
- Dialogue goes in its own labelled block under the prose, with consistent speaker names. Keep lines short enough for the clip: one or two exchanges in 4 seconds. For silent shots, give one small sound cue. (prompting-guide#Dialogue and Audio)
- Image reference: pass `input_reference` in `POST /v1/videos`; it must match the video `size` and be JPEG, PNG, or WebP, and it anchors the first frame. The prompt then describes what happens next. (prompting-guide#Use image input for more control)
- Characters: upload a 2-4 second MP4 (720p-1080p, 16:9 or 9:16), pass its ID in `characters` (at most two), and name the character in the prompt. (prompting-guide#Characters)
- Edits and extensions change one thing at a time; state the change and what stays fixed (lens, lighting, palette). Extend with `POST /v1/videos/extensions`. If a shot keeps failing, freeze the camera and simplify. (prompting-guide#Iterate with video edits, #Extend a video)

## sora-2
- Sizes: `720x1280` or `1280x720` only. (prompting-guide#API Parameters)
- The guide names no other difference; for higher resolution, switch to sora-2-pro. (prompting-guide#API Parameters)

## sora-2-pro
- Adds `1024x1792`, `1792x1024`, `1080x1920`, `1920x1080`, besides the two 720p sizes. (prompting-guide#API Parameters)
- Higher resolution renders detail and lighting transitions more accurately; reference images must match the chosen `size`. (prompting-guide#Video Resolution, #Use image input for more control)
