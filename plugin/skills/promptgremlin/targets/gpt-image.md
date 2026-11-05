---
family: gpt-image
kind: tool
last_verified: 2026-10-01
sources: [image-prompting]
---
## All models
- Keep prompt text and API settings apart. `model`, `quality` (`auto`, `low`, `medium`, `high`, `xhigh`, `max`), `size`, `background` (`auto`, `opaque`, `transparent`), `n`, `output_format` are request parameters; hand them back as a settings line beside the prompt, never as prose. (image-prompting#Model parameters)
- `size` is `auto` or `WIDTHxHEIGHT`: edges at most 3,840 px and multiples of 16, long:short ratio at most 3:1, 655,360 to 8,294,400 pixels. Examples: `1024x1536` portrait, `1536x1024` landscape, `3840x2160` 4K. (image-prompting#Model parameters)
- Say what the image is for (product photo, ad, diagram), then composition. For complex scenes use labelled sections: scene, subject, details, constraints. (image-prompting#Prompting fundamentals)
- Describe what's visible: materials, light, colors, medium. Write "photorealistic" or "real photograph" when wanted; camera specs only suggest a look. For people, give framing, gaze, and how hands touch objects. (image-prompting#Prompting fundamentals)
- Exact text: put the copy in quotes, say where it sits, how many times, and its typography; spell odd brand names letter by letter; ask for no extra text. Small or dense text needs `medium` or `high`. (image-prompting#Prompting fundamentals, #Render exact text)
- Edits: say "change only X" and list what must stay (identity, geometry, layout, lighting, labels), plus exclusions like watermarks. Number each reference image and give its role. (image-prompting#Prompting fundamentals)
- One change per turn, repeating the details to keep. For regions that must stay pixel-identical, tell the user to composite the edit onto the original. (image-prompting#Refine an image across turns, #Migrate an existing workflow)
- Transparent cutouts need the subject isolated in the prompt and `background="transparent"` set, saved as PNG or WebP; a painted checkerboard is not transparency. (image-prompting#Create a transparent product cutout)
- Slides and charts: write an artifact spec with the canvas, the real labels and numbers, and the visual language; use a landscape size and `quality="high"` for small text. UI mockups read as a shipped product, not concept art. (image-prompting#Build slides, diagrams, and charts, #Create an interface preview)
- Name the place and date for historical scenes; recurring characters keep their defining details in every prompt. (image-prompting#Use historical and real-world context, #Keep a character consistent)

## gpt-image-2-5-flare
- API id `gpt-image-2.5-flare`: the small, speed-first model, with GPT Image 2-level quality. (image-prompting#Overview, #Model parameters)
- Start here for speed or an existing GPT Image 2 workflow that already passes. Keep prompt, references, size, and quality fixed when comparing it with Sunburst. (image-prompting#Choose a model)

## gpt-image-2-5-sunburst
- API id `gpt-image-2.5-sunburst`: the base, quality-first model, above GPT Image 2. (image-prompting#Overview, #Model parameters)
- Pick it for hard cases where GPT Image 2 fell short. Keep it only if Flare can't meet the same requirements. (image-prompting#Choose a model)
- The same `quality` label doesn't mean equal quality or latency across the two. (image-prompting#Model parameters)
