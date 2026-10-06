---
family: nano-banana
kind: tool
last_verified: 2026-10-01
sources: [image-generation]
---
## All models
- Prompt text is the picture description; size, aspect ratio, and output type are API settings. Output them on a separate settings line using `response_format` fields: `type` "image", `mime_type`, `aspect_ratio` (for example "16:9"), `image_size` with an uppercase K ("2K"; "2k" is rejected). With no setting, output matches the input image's size, otherwise 1:1. Text plus image is the default reply; an image-only `response_format` drops the commentary. (image-generation#Generate images up to 4K resolution, #Optional configurations)
- Say what the image is for ("logo for a premium skincare brand") and describe the scene fully; detail buys control. Build photo prompts from shot type, subject, setting, light, camera angle, lens; illustrations from style, subject and action, medium, line or shading traits, color or background. (image-generation#Best practices, #Prompts for generating images)
- Use camera language for composition (wide-angle, macro, low angle). For busy scenes, order the build: background first, then foreground, then the small details. (image-generation#Best practices)
- Phrase exclusions as the wanted scene ("an empty street at dawn") instead of "no cars". (image-generation#Best practices)
- Text inside images: give the exact string in quotes, describe the typeface in words, and state the layout and colors. For longer copy, generate the wording in text first and then ask for the image. (image-generation#Prompts for generating images, #Limitations)
- Backgrounds meant for overlaid text: say where the subject sits in the frame and that the rest stays empty. Product shots: name the surface, the lighting setup and why, and the angle. (image-generation#Prompts for generating images)
- Edit prompts say what changes and what must stay unchanged, for example "change only the jacket to red; keep pose, lighting, and composition identical". The model then matches the original's style, lighting, and perspective. (image-generation#Prompts for editing images)
- Style transfer: name the target style and say to keep the original composition. Multi-image composites: say which element comes from which image and what the final scene is. (image-generation#Prompts for editing images)
- Iterate over several turns with small changes; that is the recommended way to refine. A requested number of images is not always honored. (image-generation#Multi-turn image editing, #Limitations)
- Audio input is unsupported; video input works only on the two 3.1 models. Best language support: English and a listed set including Spanish, French, German, Japanese, Korean, Hindi, Chinese. (image-generation#Limitations)

## Effort
- API: `thinking_level` in the generation config exists on the two 3.1 models, values `minimal` (default) and `high`. Map low and medium to `minimal`, high and max to `high`. On `gemini-3-pro-image` thinking is always on and has no control; the UI has none documented either. (image-generation#Controlling thinking levels, #Thinking process, hand-written: UI)

## gemini-3-pro-image
- Flagship (Nano Banana Pro) for professional assets and complex instructions; use it for text-heavy designs, logos, and infographics. 1K default, 2K, 4K. (image-generation#Model selection, #Prompts for generating images)
- References, up to 14 total: 6 objects, 5 characters, 3 style images. Name each image's role in the prompt. (image-generation#Use up to 14 reference images)
- Can ground in Google Search and return interleaved text and images. (image-generation#Grounding with Google Search, #Interleaved text and images)
- Ten ratios, 1:1 through 21:9; no 1:4, 4:1, 1:8, or 8:1. The source table says "3.1 Pro Image"; applying it here is assumed. (image-generation#Aspect ratios and image size, hand-written)

## gemini-3-1-flash-image
- Nano Banana 2, the recommended all-rounder for speed against quality. Sizes 512px, 1K, 2K, 4K, and the extreme ratios 1:4, 4:1, 1:8, 8:1. (image-generation#Model selection, #Aspect ratios and image size)
- References: up to 10 objects and 4 characters; no style-reference slot. Can take a video as reference for thumbnails or posters. (image-generation#Use up to 14 reference images, #Video-to-image generation)
- Search grounding covers web and image search, but not real photos of people. (image-generation#Grounding with Google Search for images, #Limitations)

## gemini-3-1-flash-lite-image
- The most efficient, low-latency, cost-effective option; 1K output only, so do not ask for 2K or 4K. No Google Search grounding. (image-generation#Generate images up to 4K resolution, #New with Gemini 3 image models)
- References: up to 14 objects, no character-consistency slot; video reference is supported. (image-generation#Use up to 14 reference images, #Video-to-image generation)
- Keep text-in-image jobs short or send them to a larger model. (hand-written)
