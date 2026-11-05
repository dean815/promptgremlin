---
family: runway
kind: tool
last_verified: 2026-10-01
sources: [text-to-video, image-to-video]
---
## All models
- First decide the mode: text-to-video (no image) or image-to-video (an image becomes the first frame). They need different prompts. Duration, ratio, and model are chosen in the app or API, not in prompt text; give them on a settings line. (hand-written; text-to-video#Core prompt elements)
- Text-to-video: cover what is seen (subject look, setting, light, framing, style) and how it moves (subject action, environment motion, camera motion, timing and speed). At minimum include one visual and one motion description. (text-to-video#Core prompt elements)
- Text-to-video template: camera framing, then subject doing an action, then the setting, then supporting detail, in plain full sentences. Order is not weighted, so use it for consistency and easy iteration rather than priority. (text-to-video#Prompt structure & organization)
- Full sentences give more control than keyword lists; keywords only nudge, and the model may use them loosely. Do not stack conflicting requests in a long prompt; clarity beats length. (text-to-video#Core prompt elements, #Prompt structure & organization)
- Image-to-video: the image already supplies composition, subject, light, and style, so the prompt is almost all motion. Do not re-describe what is in the picture; refer to people and objects generically ("the woman", "the car") to say what moves. (image-to-video#Text prompt, #Image prompt)
- In image-to-video, describe the visuals only for something new that is not in the image, a drastic change, a transformation, or an interaction between elements. (image-to-video#Text prompt)
- Image-to-video template: the camera does a move while the subject does an action, then extras. (image-to-video#Prompt structure & organization)
- Timing: write events in order in words (first, then, finally), or add rough bracketed timestamps like `[00:02]`. In text-to-video, pair timestamps with a prose scene description; keep each timestamp span realistic for how long the action takes. Match the number of events to the clip duration. (text-to-video#Advanced techniques, image-to-video#Advanced techniques)
- Start simple, add detail over iterations; if an element is missing, restate it in clearer prose. (text-to-video#Core prompt elements, #FAQ)
- Unwanted cuts: raise the duration, drop cut-implying wording, or add "continuous, seamless shot". Less camera motion: say what should move, then add a locked-off camera line and minimal subject motion. (image-to-video#FAQ)
- If the input image shows implied motion (blur, mid-action pose), a contradicting motion prompt will fight it; tell the user to use a cleaner source frame. (image-to-video#FAQ)
- Longer sequences: take the last frame of a finished clip as the next image input, then join the clips in an editor. (image-to-video#Advanced techniques)

## gen-4-5
- The text-to-video guide is tuned for Gen-4.5 (the only model in the lineup); apply the rules above as written. (text-to-video#Introduction)
- Text-to-video suits free-form motion where exact character or scene consistency does not matter; when identity or composition must hold, use image-to-video. (text-to-video#FAQ)
