---
family: kling
kind: tool
last_verified: 2026-10-01
sources: [user-guide]
---
## All models
- The only source is Kling's VIDEO 3.0 user guide, an HTML page; there is no separate prompt-engineering guide, so treat the rules below as VIDEO 3.0 behaviour and keep prompts plain prose. (hand-written: HTML-only guide)
- Spell out body motion and camera motion in the prompt: who moves, what they do with their body, and how the camera follows (tracks, orbits, pushes in, holds still). Time-order the actions with "then". (user-guide#2. Image-to-Video & Element Reference, #5. 15-Second Long-Shot Generation)
- Settings are UI choices, not prompt text: the Multi-Shot switch, Custom Multi-Shot, Native Audio vs silent, 720p/1080p, and duration (3 to 15 seconds). Put them on a settings line beside the prompt. (user-guide#1. Multi-Shot Narratives, #5. 15-Second Long-Shot Generation, Kling VIDEO 3.0 Model Pricing)
- Multi-Shot on: describe the scene as coverage (wide, close-up, reverse angle) in prose and the model plans cuts. Custom Multi-Shot: label "Shot 1", "Shot 2", and so on, each with its own framing and camera, and it follows them strictly; the shot count and durations are set in the UI. (user-guide#1. Multi-Shot Narratives)
- For one uninterrupted take, say so outright: a single continuous shot, no cuts, and keep the camera behaviour consistent. (user-guide#5. 15-Second Long-Shot Generation)
- Dialogue: write each line as speaker, then a bracketed tone or manner, then the quoted line, so the model assigns lines to the right face. Name every speaker, even with three or more characters. (user-guide#3. Native Audio Output)
- Spoken languages: Chinese, English, Japanese, Korean, Spanish, mixable in one clip. Any other language is translated to English. Name a dialect or accent next to the line it applies to. (user-guide#3. Native Audio Output)
- Ambient sound and voiceover can be written into the scene as plain sentences. (user-guide#3. Native Audio Output, #4. Native-Level Text Capabilities)
- Image-to-video with an element: the element locks the character's look, and its bound voice too. If the element already has a voice, do not describe a voice in the prompt. Elements come from 2 to 4 reference images or a character video, created in the UI. (user-guide#2. Image-to-Video & Element Reference)
- On-screen text: quote the exact lettering and say what it sits on; text already in a supplied image is preserved, so tell the camera to hold on it rather than redrawing it. (user-guide#4. Native-Level Text Capabilities)
- The guide documents no negative-prompt field; state what should happen instead of what to avoid. (hand-written: no official guide)
