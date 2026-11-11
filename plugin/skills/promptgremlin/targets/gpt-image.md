---
family: gpt-image
kind: tool
last_verified: 2026-11-11
sources: [image-prompting]
---
## All models
- Keep prompt text and API settings apart. `model`, `quality` (`auto`, `low`, `medium`, `high`, `xhigh`, `max`), `complexity` (`low`, `medium`, `high`; default `high`), `size`, `background` (`auto`, `opaque`, `transparent`), `output_format` (`png`, `jpeg`, `webp`; generations also `svg`, `gif`) are request parameters; hand them back as a settings line beside the prompt, never as prose. (image-prompting#Model parameters)
- `size` is `auto` or `WIDTHxHEIGHT`: both edges multiples of 16, aspect ratio between 1:3 and 3:1. (image-prompting#Model parameters)
- `complexity` is planning depth: default for open briefs and complex layouts, `low` for a one-detail edit. Change it or `quality`, not both; unreadable small text is a `quality` problem. (image-prompting#Model parameters, #Compare complexity)
- Say what the image is for (product photo, ad, diagram), then composition. For complex scenes use labelled sections: scene, subject, details, constraints. (image-prompting#Prompting fundamentals)
- Describe what's visible: materials, light, colors, medium. Write "photorealistic" or "real photograph" when wanted; camera specs only suggest a look. For people, give framing, gaze, and how hands touch objects. (image-prompting#Prompting fundamentals)
- Exact text: put the copy in quotes, say where it sits, how many times, and its typography; spell odd brand names letter by letter; ask for no extra text. Small or dense text needs `medium` or `high`. (image-prompting#Prompting fundamentals, #Render exact text)
- Edits: say "change only X" and list what must stay (identity, geometry, layout, lighting, labels), plus exclusions like watermarks. Number each reference image and give its role. (image-prompting#Prompting fundamentals)
- A local edit can send a `markup` overlay (transparent PNG sized like the first input, no `mask`) circling the object. (image-prompting#Guide an edit with markup)
- One change per turn, repeating the details to keep. For regions that must stay pixel-identical, tell the user to composite the edit onto the original. (image-prompting#Refine an image across turns, #Migrate an existing workflow)
- Transparent cutouts need the subject isolated in the prompt and `background="transparent"` set, saved as PNG or WebP; a painted checkerboard is not transparency. (image-prompting#Create a transparent product cutout)
- Scalable logo: `output_format="svg"`, `n=1`. Looping GIF: give a starting pose to return to and say whether the camera moves. (image-prompting#Generate SVG output, #Generate a looping GIF)
- Slides and charts: write an artifact spec with the canvas, the real labels and numbers, and the visual language; use a landscape size and `quality="high"` for small text. (image-prompting#Build slides, diagrams, and charts)

## gpt-image-2-6-flare
- API id `gpt-image-2.6-flare`: the smaller model, for when response time matters most. (image-prompting#Overview, #Model parameters)
- Start here for speed, for a GPT Image 2 workflow that already passes, or coming from 2.5 Flare. If Sunburst passes, retry Flare with the same inputs and settings. (image-prompting#Choose a model)

## gpt-image-2-6-sunburst
- API id `gpt-image-2.6-sunburst`: the base model, for more detail or precise edits. (image-prompting#Overview, #Model parameters)
- Pick it when detail, layout, or edit accuracy is demanding, where GPT Image 2 fell short, or coming from 2.5 Sunburst. (image-prompting#Choose a model)

## gpt-image-2-5-flare
- Previous generation: test 2.6 Flare first, with prompt, references, size, quality, and format unchanged. Leave out `complexity`, `markup`, `svg`, `gif`; support here is unverified. (image-prompting#Migrate an existing workflow, hand-written)

## gpt-image-2-5-sunburst
- Previous generation: test 2.6 Sunburst first, same fixed settings; the new parameters are unverified here too. (image-prompting#Migrate an existing workflow, hand-written)
