---
family: nano-banana
kind: tool
last_verified: 2026-10-12
sources: [image-generation]
---
## All models
- Prompt text is the picture description; size, aspect ratio, and output type are API settings in `response_format`: `type` "image", `aspect_ratio` (e.g. "16:9"), `image_size` with uppercase K ("2K"; "2k" is rejected). Unset, output matches the input image's size, else 1:1. Default reply is text plus image; an image-only format drops the commentary. (image-generation#Generate images up to 4K resolution, #Output format, #Aspect ratios and image size)
- Nano Banana 2.1 (`gemini-nano-banana-2.1`) is the recommended default for new work: Flash speed, better text and multi-turn consistency, 1K to 4K, web and image search grounding. (image-generation#Model selection)
- Say what the image is for and describe the scene fully; detail buys control. Photo prompts: shot type, subject, setting, light, camera angle, lens. Illustrations: style, subject and action, medium, line or shading traits, color or background. (image-generation#Best practices, #Prompts for generating images)
- Use camera language for composition (wide-angle, macro, low angle). For busy scenes, build in steps: background, then foreground, then small details. Phrase exclusions as the wanted scene ("an empty street") instead of "no cars". (image-generation#Best practices)
- Text in images: quote the exact string, describe the typeface in words, state layout and colors. For longer copy, write the wording first, then ask for the image. (image-generation#Prompts for generating images, #Limitations)
- Text-overlay backgrounds: say where the subject sits and that the rest stays empty. Product shots: name the surface, the lighting setup and its purpose, and the angle. (image-generation#Prompts for generating images)
- Edits say what changes and what stays identical; the model matches the original's style, light, and perspective. Describe critical details (a face, a logo) closely so they survive. Composites: say which element comes from which image. (image-generation#Prompts for editing images)
- Character turnarounds: ask for one angle per turn and feed earlier outputs back in; add a pose reference for hard poses. (image-generation#Prompts for editing images)
- Refine over several turns with small changes. A requested image count is not always honored. No audio input. Best languages: English plus a listed set incl. Spanish, French, German, Japanese, Korean, Hindi, Chinese. (image-generation#Best practices, #Limitations)

## Effort
- `thinking_level` exists on 3.1 Flash and 3.1 Flash Lite: `minimal` (default) or `high`; map low and medium to `minimal`, high and max to `high`. Nano Banana 2.1 adds `medium` as its default. `gemini-3-pro-image` always thinks with no control; the UI has none documented. (image-generation#Thinking process, hand-written: UI)

## gemini-nano-banana-2-1
- Nano Banana 2.1, the recommended default for new work: Flash speed and cost with better visual quality, text rendering and multi-turn consistency. Prefer it unless the job needs Pro's world knowledge or precise brand control. (image-generation#Model selection)
- Sizes 1K, 2K, 4K across fourteen ratios, including 1:4, 4:1, 1:8 and 8:1. (image-generation#Nano Banana 2.1)
- Grounding can use web search and image search together; a video can serve as the reference. (image-generation#Grounding with Google Search for images (Nano Banana 2.1 and 3.1 Flash), #Video-to-image generation (Nano Banana 2.1, 3.1 Flash, and 3.1 Flash Lite))

## gemini-3-pro-image
- Nano Banana Pro: the premium pick for hard jobs needing world knowledge, localization, brand consistency, or precise control; best for text-heavy designs, logos, infographics, comic panels. 1K default, 2K, 4K. (image-generation#Model selection, #Prompts for generating images)
- References, up to 14 total: 6 objects, 5 characters, 3 style images. Name each image's role in the prompt. (image-generation#Use up to 14 reference images)
- Web Search grounding for real-time subjects (image results are not used); can interleave text and images. (image-generation#Grounding with Google Search, #Thinking process)
- Ten ratios, 1:1 through 21:9; no 1:4, 4:1, 1:8, or 8:1. The table is headed "3.1 Pro Image"; applying it here is assumed. (image-generation#Aspect ratios and image size, hand-written)

## gemini-3-1-flash-image
- Nano Banana 2, now the previous-generation workhorse; new projects should use Nano Banana 2.1. Sizes 512px, 1K, 2K, 4K, plus ratios 1:4, 4:1, 1:8, 8:1. Good for comic panels. (image-generation#Model selection, #Aspect ratios and image size, #Prompts for generating images)
- References: up to 10 objects and 4 characters; no style slot. A video can be the reference for thumbnails, posters, or recap art. (image-generation#Use up to 14 reference images, #Video-to-image generation (Nano Banana 2.1, 3.1 Flash, and 3.1 Flash Lite))
- Search grounding covers web and image search, but not real photos of people. (image-generation#Grounding with Google Search for images (Nano Banana 2.1 and 3.1 Flash), #Limitations)

## gemini-3-1-flash-lite-image
- Nano Banana 2 Lite: fastest and cheapest, for speed and scale. Not tuned for many references or multi-turn editing, so keep jobs one-shot. 1K only; ten ratios, 1:1 to 21:9. No search grounding. (image-generation#Model selection, #Features of Nano Banana)
- References: up to 14 objects, no character slot; video reference is supported. (image-generation#Use up to 14 reference images, #Video-to-image generation (Nano Banana 2.1, 3.1 Flash, and 3.1 Flash Lite))
- Keep text-in-image jobs short or send them to a larger model. (hand-written)
