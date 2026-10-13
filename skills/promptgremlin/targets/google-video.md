---
family: google-video
kind: tool
last_verified: 2026-10-12
sources: [veo, omni, flow]
---
## All models
- Default to Gemini Omni Flash; use Veo for a Veo-only control: `durationSeconds` of 4/6/8, extension chains to 148s, up to three `referenceImages`. Keep model and settings on a separate line. (veo#Veo API parameters and specifications; hand-written: choice rule)
- Omni settings: `aspect_ratio` ("16:9" default, "9:16"), `resolution` in `response_format` (`360p`, `720p` default, `1080p` and `4k` upscaled), and `task` (`image_to_video`, `edit`, `extend`, etc.), left unset unless prompting alone fails. Veo: `aspectRatio`, `durationSeconds`, `resolution`. None belong in prose. (omni#Control aspect ratio, #Output resolution, #Tasks parameter, veo#Veo API parameters and specifications)
- Describe the shot as subject, action, style, then optional camera position or move, framing, focus or lens, and color and light mood, with vivid adjectives. To push facial detail, call it a portrait. (veo#Prompt writing basics)
- Timing: plain words ("after 3 seconds...", "every 2s cut") or one timecode line per segment, like `[0-3s] ...`. (omni#Timing events)
- Audio is always generated. Put dialogue in quotes, spell out sound effects and ambience, and name any music explicitly. Write exclusions as prose ("No dialogue"); there is no negative-prompt field. (veo#Prompting for audio, omni#Prompting the audio, #Removing unwanted elements, #Limitations)
- On-screen text: quote the exact words, including signs or plates that would appear anyway. (omni#Text in videos)
- Omni responds to quality cues: ask for rich micro-detail, specific costume and object description, and a lived-in background. (omni#Meta prompting)
- Image-to-video: name the camera move, subject motion, and environment effects, not "make it move". (omni#Image to video generation)
- Flow: `@Name` calls a saved character (`@me` = your avatar); frames and ingredients are picked in the model menu. Describe the transition between start and end frames and how each ingredient is used. (flow#Add start & end frames to your prompt, #Add characters to your prompt, #Add visual references to your prompt)
- Flow ingredients: subjects on plain backgrounds, no stray subjects in style or location refs, one consistent look; mention every input and never contradict it. `@Voice: Name` works only with ingredients on Omni Flash. (flow#Best practices & advanced tips when generating in Google Flow, #Add voice references to your prompt)

## gemini-omni-1-1-flash
- Flagship. It cuts between shots by default; for one take, ask for one unbroken shot. (omni#Single scene)
- Edits: one short instruction per turn plus "Keep everything else the same"; long ones cause stray changes. (omni#Prompts for editing)
- Bind inputs with tags: `<FIRST_FRAME>`, `<LAST_FRAME>` (needs a first frame; same image both ends loops), `<IMAGE_REF_N>`, `<VIDEO_REF_N>` from 0; complex jobs declare `[# Sources ...]` / `[# References ...]` first. (omni#Using tags in prompts to set image and video roles)
- Extension: +10s to 40s total from the last 10s; say if the scene continues or cuts and what the audio does; 0s is the new part's start. (omni#Prompts for extending a video)
- No audio refs, voice edits, or multi-video prompts; video refs max 3 clips of 3s. (omni#Limitations)

## veo-3-1-generate-preview
- Preview. Prompt text up to 1,024 tokens. `durationSeconds` "4", "6", "8"; 8 is required with 1080p, 4k, extension, or reference images. (veo#Veo 3.1 Preview, #Veo API parameters and specifications)
- First and last frames: pass `lastFrame` with `image`, and write the action between them. Up to three `referenceImages` of one person, character, or product keep its look. (veo#Using first and last frames, #Prompting with reference images)
- Extension: adds 7 seconds, up to 20 times, to a Veo-made 720p clip, 148 seconds total at most; it continues the final second, and speech only carries over if present in it. (veo#Extending Veo videos, #Prompting for extension)

## veo-3-1-fast-generate-preview
- Preview speed tier with the same parameters and abilities as `veo-3-1-generate-preview`, including references, `lastFrame`, extension, and 4k. Use it for quick iterations, ad variants, and social clips. (veo#Veo API parameters and specifications, #Model features, #Veo 3 Fast (Deprecated))
- Prompt text up to 1,024 tokens. (veo#Veo 3.1 Fast Preview)

## veo-3-1-lite-generate-preview
- Preview, lowest tier. Text-to-video and image-to-video with `lastFrame`; no reference images, no extension, no video input, and no 4k. 1080p needs 8 seconds. (veo#Model features, #Veo API parameters and specifications, #Extending Veo videos)
- Prompt text up to 1,024 tokens. (veo#Veo 3.1 Lite Preview)
