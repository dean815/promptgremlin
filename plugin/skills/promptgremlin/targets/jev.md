---
family: jev
kind: tool
last_verified: 2026-11-11
sources: [models, primitives]
---
## All models
- A Jev "prompt" is not prose. It is a JSON request body with `model`, `state` (the material to judge), and `questions` (a map of id to question). Output that JSON, not a chat message. (primitives#Define a question, #Ask multiple questions together)
- Question ids are not sent to the model. Put the complete meaning in `instructions`. (primitives#Define a question)
- Each question has `type`, `instructions`, and usually `criteria`. `choice`: one of an unordered set (criteria is an object of option to meaning). `score`: position on ordered levels (criteria is an ordered list, each level self-explanatory). `noul`: clean yes/no (criteria optional). `box`: locates a target in an image (Jev 1.14 only). (primitives#Define a question, #Choose a question type, #What comes back)
- A choice always picks a supplied option, even when none fits. Skip the `other` or `none` option (it competes with the real ones); add a companion `noul` asking whether any option fits. (primitives#Choose a question type, #What comes back)
- One snap judgment per question, one a person makes in a second. Split anything needing analysis into small questions; the code combines and weights them. (primitives#Ask for one snap judgment per question, #Split a complex judgment into several questions)
- Questions run in parallel and cannot see each other. Never write one that depends on another; a truly dependent one is a second request, noted outside the JSON. (primitives#When one question depends on another)
- Extra questions are nearly free and uncapped; include ones that matter only for some inputs. Use one `noul` per label when several can apply. (primitives#Ask speculative questions, #How many questions you can ask, #Choose a question type)
- Define a `noul`'s yes condition precisely; use a `score` with defined levels for degree. (primitives#Choose a question type)
- Point at parts of a structured state with backticked dot-paths such as `ticket.messages[0].text` inside `instructions`. (primitives#Reference specific fields)
- State is text (string, JSON object, or array of text) and PNG or JPEG images; no audio or video. (models#Current models)
- Shape (invented):
```json
{
  "model": "jev-latest",
  "state": { "review": "Arrived late, box crushed, works fine." },
  "questions": {
    "topic": {
      "type": "choice",
      "instructions": "What is the main complaint in `review`?",
      "criteria": {
        "shipping": "Delivery",
        "product": "Faulty item"
      }
    },
    "topic_fits": {
      "type": "noul",
      "instructions": "Is the main complaint in `review` shipping or a faulty item?"
    },
    "anger": {
      "type": "score",
      "instructions": "How angry is the writer of `review`?",
      "criteria": ["Calm", "Irritated", "Upset", "Furious"]
    }
  }
}
```

## jev-1-14-0
- Newest release and what `jev-latest` points to. Send `"model": "jev-1.14.0"` (dots) to pin it, or `jev-latest` to follow the newest stable release; the alias can change answers when a release ships. `jev-preview` can run ahead of `jev-latest`; it is the same model for now. (models#Aliases)
- The only version with `box` questions; a box always returns a location, so pair it with a `noul` asking whether the target is present. (models#Current models; primitives#What comes back)
- Budget: 64k tokens per request covering `state` plus all questions, and 32k for `state` plus any one question, so keep state and each question's `instructions` compact. A long-context request header raises both to 262k but is slower and less accurate. (models#Current models, #Context length)

## jev-1-13-0
- Previous version, pinned as `"model": "jev-1.13.0"`; same limits and inputs as 1.14 but no `box` questions. (models#Current models)
