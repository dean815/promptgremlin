---
family: higgsfield
kind: tool
last_verified: 2026-11-11
sources: [prompt-help]
---
## All models
- Higgsfield hosts many image and video models; its one official prompt article is model-agnostic. Use the rules below as the platform baseline, then follow the picked model's own notes where they exist and differ: `sora`, `google-video` (Veo), `kling`, `nano-banana`, `gpt-image`. If the model is unknown, ask which one before writing. (hand-written)
- Be specific, in layers: subject, details (appearance, clothing, expression), environment, and style; for video add camera and mood. Not every layer is needed each time, but spell out whatever matters, because vague prompts get a different guess on every run. (prompt-help#Why does being specific matter so much?)
- Image-to-video: the start image already carries character, setting, lighting, and style, so do not redescribe them. Describe what happens: action, camera movement, timing, mood. (prompt-help#Step 4: Bring the scene to life with video)
- Cinematic clips: write a shot list in labelled blocks rather than a sentence: style and mood; cinematography and camera; lighting and color; action beat by beat; audio (score, ambience, timed dialogue); then the shots with durations. (prompt-help#Step 4: Bring the scene to life with video)
- Match depth to the job: one line of motion is enough for a simple short clip; keep the full block structure for sequences that need control. (prompt-help#Step 4: Bring the scene to life with video, #What habits make any prompt better?)
- Consistency comes from references, not prose: generate the character once and reuse it. Soul ID for a real person, a saved Element referenced in the prompt for video, attached character images for image models. When restyling, state what to keep and what to change. (prompt-help#How do I keep the same character across generations?; hand-written: keep/change wording is from the page's unwatched Step 2)
- Say what should appear rather than listing what should not; a few named exclusions ("no readable text") are fine on detailed shots. (prompt-help#What habits make any prompt better?)
- Make the prompt agree with the input image; a calm, still instruction fights a motion-blurred frame. (prompt-help#What habits make any prompt better?)
- Write in English by default. Seedance and Kling can respond better to Chinese for nuanced motion. (prompt-help#What habits make any prompt better?)
- Iterate one change at a time (lighting, lens, a wardrobe detail). For longer sequences, start the next clip from the last frame of the previous one and join them in an editor. (prompt-help#How do I improve a result I don't like?)
- Camera `#` tags, camera/lens/grading presets, and Moodboard are UI selections this article does not cover; list any on a "UI selections" line beside the prompt rather than in it. (hand-written: unverified)
