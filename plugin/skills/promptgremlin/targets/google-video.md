---
family: google-video
kind: tool
last_verified: 2026-11-11
sources: [veo, omni, flow]
---
## All models
- Default to Gemini Omni Flash. The Veo 3.1 preview ids were shut down in the Gemini API on 2026-10-22; write for Veo only where it is still served. Its extras: `durationSeconds` of 4/6/8, extension chains to 148s, three `referenceImages`. Keep model and settings on a separate line. (veo#Veo API parameters and specifications; hand-written: choice rule, veo page intro)
- Omni settings: `aspect_ratio` ("16:9" default, "9:16"); in `response_format`, `resolution` (`360p`, `720p` default, `1080p` and `4k` upscaled) and `duration` ("3s" to "15s", default 10s, beats any length in the prompt; 10s cap with first and last frames); and `task` (`image_to_video`, `edit`, `extend`, etc.), left unset unless prompting alone fails. Veo: `aspectRatio`, `durationSeconds`, `resolution`. None belong in prose. (omni#Control aspect ratio, #Output resolution, #Control video duration, #Tasks parameter, veo#Veo API parameters and specifications)
- Describe the shot as subject, action, style, then optional camera position or move, framing, focus or lens, and color and light mood, with vivid adjectives. To push facial detail, call it a portrait. (veo#Prompt writing basics)
- Timing: plain words ("after 3 seconds...", "every 2s cut") or one timecode line per segment, like `[0-3s] ...`. (omni#Timing events)
- Audio is always generated. Put dialogue in quotes, spell out sound effects and ambience, and name any music explicitly. Write exclusions as prose ("No dialogue"); Omni has no negative-prompt field and takes no system instruction. (veo#Prompting for audio, omni#Prompting the audio, #Removing unwanted elements, #Limitations)
- On-screen text: quote the exact words, including signs or plates that would appear anyway. (omni#Text in videos)
- Omni responds to quality cues: ask for rich micro-detail, specific costume and object description, and a lived-in background. (omni#Meta prompting)
- Image-to-video: name the camera move, subject motion, and environment effects, not "make it move". (omni#Image to video generation)
- Flow: `@Name` calls a saved character (`@me` = your avatar); frames and ingredients are picked in the model menu. Describe the transition between start and end frames and how each ingredient is used. (flow#Add start & end frames to your prompt, #Add characters to your prompt, #Add visual references to your prompt)
- Flow ingredients: subjects on plain backgrounds, no stray subjects in style or location refs, one consistent look; mention every input and never contradict it. `@Voice: Name` works only with ingredients on Omni Flash. (flow#Best practices & advanced tips when generating in Google Flow, #Add voice references to your prompt)

## gemini-omni-1-2-flash
- Flagship. It cuts between shots by default; for one take, ask for one unbroken shot. (omni#Single scene)
- Edits: one short instruction per turn plus "Keep everything else the same"; long ones cause stray changes. (omni#Prompts for editing)
- Say in plain words what each input is for; control tags like `<FIRST_FRAME>` are deprecated. Up to 6 reference images; reference videos (3s, new clips only): 3 for clips up to 10s, 1 above. No audio refs or voice edits. (omni#Tasks parameter, #Limitations)
- Extension: +3 to 10s per turn to 30s total, from the last 10s; re-describe anything seen only earlier, say if the scene continues or cuts and what the audio does; 0s is the new part's start. (omni#Prompts for extending a video, #Extension constraints and guidelines)

## gemini-omni-1-1-flash
- Previous version: from 2026-12-03 requests to this id route to 1.2. Write the prompt as for 1.2, with plain-language input roles and no control tags. (hand-written: omni page intro; omni#Tasks parameter)
- The page now documents only 1.2; whether 1.1 accepts `duration` up to 15s, six reference images, or the 30s extension cap is not stated (unverified). (hand-written)

## veo-3-1-generate-preview
- Preview, shut down in the Gemini API on 2026-10-22. Prompt text up to 1,024 tokens. `durationSeconds` "4", "6", "8"; 8 is required with 1080p, 4k, extension, or reference images. (veo#Model versions, #Veo API parameters and specifications; hand-written: shut-down notice)
- First and last frames: pass `lastFrame` with `image`, and write the action between them. Up to three `referenceImages` of one person, character, or product keep its look. (veo#Using first and last frames, #Prompting with reference images)
- Extension: adds 7 seconds, up to 20 times, to a Veo-made 720p clip, 148 seconds total at most; it continues the final second, and speech only carries over if present in it. (veo#Extending Veo videos, #Prompting for extension)

## veo-3-1-fast-generate-preview
- Preview speed tier, shut down in the Gemini API with the rest of Veo 3.1, with the same parameters and abilities as `veo-3-1-generate-preview`, including references, `lastFrame`, extension, and 4k. Use it for quick iterations, ad variants, and social clips. (veo#Veo API parameters and specifications, #Model features, #Model versions; hand-written: shut-down notice)
- Prompt text up to 1,024 tokens. (veo#Model versions)

## veo-3-1-lite-generate-preview
- Preview, lowest tier, also shut down in the Gemini API. Text-to-video and image-to-video with `lastFrame`; no reference images, no extension, no video input, and no 4k. 1080p needs 8 seconds. (veo#Model features, #Veo API parameters and specifications, #Extending Veo videos; hand-written: shut-down notice)
- Prompt text up to 1,024 tokens. (veo#Model versions)
